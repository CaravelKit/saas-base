import Sample_long_page from './views/Sample_long_page.vue';
import Simple_elements from './views/UI_Element_library_Simple_elements.vue';


var userRoutes = [
    { 
        path: '/sample', 
        name: 'Sample_long_page',
        component: Sample_long_page,
        meta: {
            breadcrumb: [{name: 'Sample long page', route: 'Sample_long_page'}]
        }
        
    },
    { 
        path: '/library/simple', 
        name: 'Simple_elements',
        component: Simple_elements,
        meta: {
            breadcrumb: [{name: 'UI Element library', route: 'UI_Element_library'}, 
                {name: 'Simple elements', route: 'Simple_elements'}
            ]
        }
        
    },
    ];

export default userRoutes;