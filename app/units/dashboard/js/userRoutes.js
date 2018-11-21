import SamplePage from './views/samplePage.vue';
import SampleTable from '../components/component1/views/table.vue';


var userRoutes = [
    { 
        path: '/dashboard/samplePage', 
        name: 'SamplePage',
        component: SamplePage,
        meta: {
            breadcrumb: [{name: 'Sample page', route: 'SamplePage'}]
        }
        
    },
    { 
        path: '/dashboard/sampleTable', 
        name: 'SampleTable',
        component: SampleTable,
        meta: {
            breadcrumb: [{name: 'Sample table', route: 'SampleTable'}]
        }
        
    }
];

export default userRoutes;