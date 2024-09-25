from collections import namedtuple, ChainMap
from datetime import datetime
import yaml
import os, sys
import traceback
import importlib
from mlflow.models.signature import infer_signature
from .mlflow import MLflowModel

EthicsType   = namedtuple('BaseEthicsType', 'ethics_type_enum sensitive_predictor_columns label_column')
EthicsResult = namedtuple('BaseEthicsResult', 'ethics_type result_str risk')
DriftType    = namedtuple('BaseDriftType', 'drift_type_enum model_instance data_array')
DriftResult  = namedtuple('BaseDriftResult', 'drift_type result_str')

class Trainer():
    def __init__(self, path: str = './', verbose: bool = False):
        self._verbose       = verbose
        self._error_message = None
        self._path          = path
        
    def _load_cortex_yaml(self):
        """
        Loads a model's cortex.yaml file.
        """
        with open(os.path.join(self._path, 'cortex.yml'), 'r') as file:
            config = yaml.safe_load(file)

        steps_key = 'training_steps' if 'training_steps' in config.keys() else 'pipeline_steps'

        steps = {}
        for item in config[steps_key]:
            key, value = list(item.items())[0]
            steps[key] = value

        config['training_steps'] = steps

        config['modules'] = {}
        walk_path = '.'
        if 'module_path' in config.keys() and config['module_path'] is not None:
            config['module_path'] = os.path.join(self._path, f'{config["module_path"][2:]}')
            walk_path = config['module_path']
        for (root, dir_names, file_names) in os.walk(walk_path):
            file_names[:] = [
                f for f in file_names 
                if f.endswith('.py') and f not in ['__init__.py', '{}.py'.format(walk_path)] 
            ]
            # TODO: Set map of file path locations to module name
            for f in file_names:
                config['modules']['{}/{}'.format(root, f)] = f.replace('.py', '')

        return config

    
    def _initialize_steps(self):
        # Add default initialize model and download data steps
        _steps = [
            {
                'name':   'Initialize model class',
                'type':   '_instantiate_model',
                'config': {
                    'cortex_cli_func': True
                }
            }
        ]

        for key, value in self._cortex_config['training_steps'].items():
            _steps.append({
                'name':   value,
                'type':   key,
                'config': {}
            })
        
        # Add default download data step
        _steps.append({
            'name':   'Cleanup model params',
            'type':   'cleanup_self',
            'config': {}
        })

        # Add default save pipeline artifacts step
        _steps.append({
            'name':   'Save pipeline artifacts',
            'type':   '_save_pipeline',
            'config': {
                'cortex_cli_func': True
            }
        })
        
        # Set steps
        self._steps = _steps

        print('Loaded pipeline steps')
    
    def _run_training_steps(self):
        current_step = None
        try:
            for step in self._steps:
                current_step = step['type']
                step_config  = step['config']
                step_func    = getattr(self if step_config.get('cortex_cli_func') else self.model, current_step)
                
                if self._verbose:
                    print(f'Running step: {step["name"]} ({current_step})')

                step_result = step_func()

                if self._verbose:
                    print(f'Step result: {step_result}')

                print(f'{step["name"]} completed successfully')
        except Exception as e:
            self._error_message = f'{step["name"]} completed with an error.\n{traceback.format_exc()}'
            raise Exception
    

    def get_model_params(self):
        if 'model_params' not in self.__dict__.keys():
            self.model_params = dict(ChainMap(*self._cortex_config['params'])) if self._cortex_config['params'] else {}

        return self.model_params


    def set_model_param(self, key, value):
        model_params = self.get_model_params()
        model_params[key] = value
        self.model_params = model_params

        return self.model_params


    def _instantiate_model(self):
        # LOAD DEPENDENCY MODULES (except model)
        for path, module in self._cortex_config['modules'].items():
            self._load_module(path, module)

        # LOAD MODEL MODULE
        if 'module_path' in self._cortex_config.keys() and self._cortex_config['module_path'] is not None:
            path = os.path.join(self._path, path)
            
            model_module = self._load_module(
                '{}/{}.py'.format(os.path.join(self._path, self._cortex_config['module_path'])),
                self._cortex_config['model_module']
            )
        else:
            model_module = self._load_module(
                '{}/{}.py'.format(self._path, self._cortex_config['model_module']),
                self._cortex_config['model_module']
            )

        model_params = self.get_model_params()

    def _load_module(self, module_path, module_name):
        print('\t\tLoading module {} from {}'.format(module_name, module_path))
        spec                     = importlib.util.spec_from_file_location(module_name, module_path)
        module                   = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    
    def _save_pipeline(self):
        print('Saving pipeline artifacts...')

        # Save model
        modules = list(self._cortex_config['modules'].keys())
       # modules.append(self._cortex_config['model_module'])
        if self.model.model_type == 'cortex':
            MLflowModel.save_model(
                python_model     = self.model, 
                path             = self._artifacts_dir,                   # Where artifacts are stored locally
                code_path        = modules,                    # Local code paths not on
                conda_env        = 'conda.yml',
                signature        = infer_signature(self.model.input_example, self.model.output_example),
                training_steps   = self._cortex_config['training_steps'],
                deployment_steps = self._cortex_config.get('deployment_steps') or []
            )
        else:
            self._error_message = f"An error occurred while detecting the Cortex model type. \
            Found '{self.model.model_type}', but only ['cortex'] are acceptable values"
            raise Exception

        return f'Saved the pipeline artifacts to disk: ({self._artifacts_dir})'
    

    def set_artifacts_dir(self, artifacts_dir: str = None):
        if artifacts_dir is not None:
            self._artifacts_dir = artifacts_dir
            return self._artifacts_dir
        
        location = 'cortex' if self._use_tracking else 'local'
        id = self._pipeline_id if self._use_tracking and self._pipeline_id else self._now
        self._artifacts_dir =  f'models/{location}/{id}'

        return self._artifacts_dir
    
    @property
    def _now(self):
        return datetime.now().strftime('%m%d%Y-%H%M%S')

    #---------------------------------------------------------------------------

    def from_file(self, path: str):
        self._path          = path
        self._cortex_config = self._load_cortex_yaml()

        return self

    def run(self, artifacts_dir: str = None):
        try:
            self.set_artifacts_dir(artifacts_dir)

            # Step 3 - Initialize the pipeline steps
            self._initialize_steps(self._pipeline_id)

            # Step 4 - Run the pipeline
            if self._use_tracking:
                self._run_pipeline(
                    self._pipeline_id,
                    self._model_id
                )

            # Step 5 - Run the training steps
            self._run_training_steps()

        except Exception as e:
            # Handle extra errors in cases we haven't yet caught
            if not self._error_message:
                self._error_message = traceback.format_exc()

        finally:
            if self._error_message:
                print(self._error_message)
            else:
                print('Completed Cortex Pipeline Run')
