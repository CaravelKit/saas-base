import Route_with_href11 from './views/Route_with_href11.vue';
import Route_with_href_and_params from './views/Route_with_href_and_params.vue';
import SamplePage from './views/SamplePage.vue';
import Complex_menu_with_href from './views/Complex_menu_with_href.vue';
import Subpage_with_href from './views/Complex_menu_with_href_Subpage_with_href.vue';
import Brands_options_auto from './views/Complex_menu_with_href_Brands_options_auto.vue';
import Subpage_without_href from './views/Complex_menu_with_href_Subpage_without_href.vue';
import Menu_without_href from './views/Menu_without_href.vue';
import aaa from './views/Menu_without_href_aaa.vue';
import bbb from './views/Menu_without_href_bbb.vue';
import Menu_suto from './views/Menu_suto.vue';
import aaa1 from './views/Menu_suto_aaa1.vue';
import bbb1 from './views/Menu_suto_bbb1.vue';


var userRoutes = [
    { 
        path: '/table', 
        name: 'Route_with_href11',
        component: Route_with_href11,
        meta: {
            breadcrumb: [{name: 'Route with href11', route: 'Route_with_href11'}]
        }
        
    },
    { 
        path: '/table/:userId', 
        name: 'Route_with_href_and_params',
        component: Route_with_href_and_params,
        meta: {
            breadcrumb: [{name: 'Route with href and params', route: 'Route_with_href_and_params', params: { userId: 123 }}]
        }
        
    },
    { 
        path: '/dashboard/SamplePage', 
        name: 'SamplePage',
        component: SamplePage,
        meta: {
            breadcrumb: [{name: 'Menu with auto href', route: 'SamplePage'}]
        }
        
    },
    { 
        path: '/sample', 
        name: 'Complex_menu_with_href',
        component: Complex_menu_with_href,
        meta: {
            breadcrumb: [{name: 'Complex menu with href', route: 'Complex_menu_with_href'}]
        }
        
    },
    { 
        path: '/billing', 
        name: 'Subpage_with_href',
        component: Subpage_with_href,
        meta: {
            breadcrumb: [{name: 'Complex menu with href', route: 'Complex_menu_with_href'}, 
                {name: 'Subpage with href', route: 'Subpage_with_href'}
            ]
        }
        
    },
    { 
        path: '/dashboard/Brands_options_auto', 
        name: 'Brands_options_auto',
        component: Brands_options_auto,
        meta: {
            breadcrumb: [{name: 'Complex menu with href', route: 'Complex_menu_with_href'}, 
                {name: 'Brands options auto', route: 'Brands_options_auto'}
            ]
        }
        
    },
    { 
        path: '#', 
        name: 'Subpage_without_href',
        component: Subpage_without_href,
        meta: {
            breadcrumb: [{name: 'Complex menu with href', route: 'Complex_menu_with_href'}, 
                {name: 'Subpage without href', route: 'Subpage_without_href'}
            ]
        }
        
    },
    { 
        path: '#', 
        name: 'Menu_without_href',
        component: Menu_without_href,
        meta: {
            breadcrumb: [{name: 'Menu without href', route: 'Menu_without_href'}]
        }
        
    },
    { 
        path: '#', 
        name: 'aaa',
        component: aaa,
        meta: {
            breadcrumb: [{name: 'Menu without href', route: 'Menu_without_href'}, 
                {name: 'aaa', route: 'aaa'}
            ]
        }
        
    },
    { 
        path: '#', 
        name: 'bbb',
        component: bbb,
        meta: {
            breadcrumb: [{name: 'Menu without href', route: 'Menu_without_href'}, 
                {name: 'bbb', route: 'bbb'}
            ]
        }
        
    },
    { 
        path: '/dashboard/Menu_suto', 
        name: 'Menu_suto',
        component: Menu_suto,
        meta: {
            breadcrumb: [{name: 'Menu suto', route: 'Menu_suto'}]
        }
        
    },
    { 
        path: '#', 
        name: 'aaa1',
        component: aaa1,
        meta: {
            breadcrumb: [{name: 'Menu suto', route: 'Menu_suto'}, 
                {name: 'aaa1', route: 'aaa1'}
            ]
        }
        
    },
    { 
        path: '#', 
        name: 'bbb1',
        component: bbb1,
        meta: {
            breadcrumb: [{name: 'Menu suto', route: 'Menu_suto'}, 
                {name: 'bbb1', route: 'bbb1'}
            ]
        }
        
    },
    ];

export default userRoutes;