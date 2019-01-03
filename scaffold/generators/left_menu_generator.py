import os.path
from yaml import load, dump
import requests
import json
from flask import current_app

from app import get_path_to_include
from . import common
    
def generate_code(yaml_name):
    # 1. Read the Yaml file to verify its existence and validity
    print('Reading Yaml configuration...')
    file_yaml_name = yaml_name + '.yaml'
    #file_yaml_name = get_path_to_include(r'..\\scaffold\\' + file_yaml_name)
    file_yaml_name = os.path.abspath(r'scaffold\\' + file_yaml_name)

    if not os.path.exists(file_yaml_name):
        raise Exception(file_yaml_name + ' file not found! Please create in the /scaffold folder')
    stream = open(file_yaml_name, 'rt')
    
    yaml_object = load(stream) # If yaml file is not valid, exception will be raised
    if not yaml_object:
        stream.close()
        raise Exception('The Yaml config file is empty or non-valid, please check it.')

    stream.seek(0)

    # 2. If no exception, send to the server
    print('Requesting the server to generate...')
    api_key = current_app.config['SAAS_API_KEY']
    api_email = current_app.config['SAAS_API_EMAIL']
    api_url = '{0}/scaffold/element/{1}'.format(current_app.config['SAAS_API_URL'], yaml_name)
    headers = {
        'Content-Type': 'application/json'
    }
    #request = requests.post(api_url, files = {'yaml_config': stream})

    yaml_full = {
        'cred': {
            'key': api_key,
            'email': api_email
        },
        'menu': yaml_object['menu'],
        'meta': {
            'generate_vue_components' : (yaml_object['meta']['generate_vue_components'] 
                if yaml_object['meta']['generate_vue_components'] != None 
                else False),
            'breadcrumbs': yaml_object['meta']['breadcrumbs'],
            'components_folder': yaml_object['meta']['components_folder']
        }
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(yaml_full))
    stream.close()
    result_json = json.loads(response.text)
    if not result_json['result']:
        err_text = (', '.join(result_json.get('errors')) 
            if result_json.get('errors') is not None else '''Some error occured on the server. 
            Please retry you request. If this message 
            persists please ask for the assistance at support''')
        raise Exception(err_text)
    
    result = result_json['render']
    #print(result['interface_components_render']['components'][0]['content'])

    # 3. Update the output file - left menu itself
    print('Updating the output file...')
    output_file_path = yaml_object['meta']['file_output']
    output_file_name = os.path.abspath(output_file_path)

    rewrite = yaml_object['meta']['rewrite'] != None and yaml_object['meta']['rewrite'] == True
    common.create_write_file(output_file_name, result['left_menu'], rewrite)

    
    # 4. If other Vue files should be created also, routes first
    output_routes_path = yaml_object['meta']['routes_file']
    routes_file_name = os.path.abspath(output_routes_path)
    common.create_write_file(routes_file_name, result['interface_components_render']['routes'], rewrite, 
        comment_start = r'/*', comment_end = r'*/')

    print('Scaffolding done.')
    # 5. Components folders/files
    for component in result['interface_components_render']['components']:
        file_component_name = (component['name'] if component['parent'] is None else (component['parent'] + 
            '_' + component['name'])) + '.vue'
        components_folder = (yaml_object['meta']['components_folder'] if ('components_folder' in yaml_object['meta'] 
            and yaml_object['meta']['components_folder'] is not None)
            else '')
        full_file_name = get_path_to_include(os.path.join(r'js\\views', components_folder, 
            file_component_name))
        print(full_file_name)
        common.create_write_file(full_file_name, 
            component['content'], 
            rewrite)

        '''
        folder_name = component['name'] if component['parent'] is None else component['parent']
        component_file_path = os.path.join(yaml_object['meta']['components_folder'], 
            folder_name,
            component['name'] + '.vue')
        component_file_name = get_path_to_include(component_file_path)
        #print(component_file_name)
        common.create_write_file(component_file_name, 
            component['content'], 
            rewrite)
        '''
    
    

if __name__ == '__main__':
    main()