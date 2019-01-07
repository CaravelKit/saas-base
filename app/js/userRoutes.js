import Sample_long_page from './views/Sample_long_page.vue';
import Simple_elements from './views/UI_Element_library_Simple_elements.vue';
import Pages from './views/Pages.vue';


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
    { 
        path: '/dashboard/Pages', 
        name: 'Pages',
        component: Pages,
        meta: {
            breadcrumb: [{name: 'Pages', route: 'Pages'}]
        }
        
    },
    ];

export default userRoutes;/*import Sample_long_page from './views/Sample_long_page.vue';
import Simple_elements from './views/UI_Element_library_Simple_elements.vue';
import Pages from './views/Pages.vue';


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
    { 
        path: '/dashboard/Pages', 
        name: 'Pages',
        component: Pages,
        meta: {
            breadcrumb: [{name: 'Pages', route: 'Pages'}]
        }
        
    },
    ];

export default userRoutes;import Sample_long_page from './views/Sample_long_page.vue';
import Simple_elements from './views/UI_Element_library_Simple_elements.vue';
import Pages from './views/Pages.vue';
import RegisterPage from './views/Pages_RegisterPage.vue';
import LoginPage from './views/Pages_LoginPage.vue';


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
    { 
        path: '/dashboard/Pages', 
        name: 'Pages',
        component: Pages,
        meta: {
            breadcrumb: [{name: 'Pages', route: 'Pages'}]
        }
        
    },
    { 
        path: '/register', 
        name: 'RegisterPage',
        component: RegisterPage,
        meta: {
            breadcrumb: [{name: 'Pages', route: 'Pages'}, 
                {name: 'Register page', route: 'RegisterPage'}
            ]
        }
        },
    { 
        path: '/login', 
        name: 'LoginPage',
        component: LoginPage,
        meta: {
            breadcrumb: [{name: 'Pages', route: 'Pages'}, 
                {name: 'Login page', route: 'LoginPage'}
            ]
        }
        },
    ];

export default userRoutes;import Sample_long_page from './views/Sample_long_page.vue';
import Simple_elements from './views/UI_Element_library_Simple_elements.vue';
import Pages from './views/Pages.vue';
import LoginPage from './views/Pages_LoginPage.vue';


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
    { 
        path: '/dashboard/Pages', 
        name: 'Pages',
        component: Pages,
        meta: {
            breadcrumb: [{name: 'Pages', route: 'Pages'}]
        }
        
    },
    { 
        path: '/dashboard/LoginPage', 
        name: 'LoginPage',
        component: LoginPage,
        meta: {
            breadcrumb: [{name: 'Pages', route: 'Pages'}, 
                {name: 'Login page', route: 'LoginPage'}
            ]
        }
        },
    ];

export default userRoutes;*/