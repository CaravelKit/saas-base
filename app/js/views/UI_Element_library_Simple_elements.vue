<template>
    <div>
        <span>All elements are based on <a href="https://getbootstrap.com/">Bootstrap 4</a></span>
        <h4 class="top-buffer-20">Table</h4>
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">First name</th>
                        <th scope="col">Last name</th>
                        <th scope="col">Position</th>
                        <th scope="col">Edit data</th>
                        <th scope="col">What to do with him/her</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Michael</td>
                        <td>Bolton</td>
                        <td>Programmer</td>
                        <td><a href="#" class="simple-link">Edit</a></td>
                        <td>
                            <button class="btn btn-danger">Fire</button>
                            <button class="btn btn-success">Promote</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Samir</td>
                        <td>Nagheenanajar</td>
                        <td>Programmer</td>
                        <td><a href="#" class="simple-link">Edit</a></td>
                        <td>
                            <button class="btn btn-danger">Fire</button>
                            <button class="btn btn-success">Promote</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Bill</td>
                        <td>Lumbergh</td>
                        <td>Vice president</td>
                        <td><a href="#" class="simple-link">Edit</a></td>
                        <td>
                            <button class="btn btn-danger">Fire</button>
                            <button class="btn btn-success">Promote</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <h4 class="top-buffer-20">Card</h4>
        <div class="card">
            <h5 class="card-header">Featured</h5>
            <div class="card-body">
                <h5 class="card-title">Special title treatment</h5>
                <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                <button class="btn btn-primary">Go somewhere</button>
            </div>
        </div>
        <h4 class="top-buffer-20">Buttons</h4>
            <div class="top-buffer-20">
                <button class="btn btn-primary">Button primary</button>
                <button class="btn btn-danger">Button danger</button>
                <button class="btn btn-success">Button success</button>
            </div>
        <h4 class="top-buffer-20"><a href="https://fontawesome.com">Font Awesome</a> at your service</h4>
            <div class="top-buffer-20">
                <div>Table tennis <i class="fas fa-table-tennis" style="color: blue; font-size:28px"></i></div>
                <div>Crhart line <i class="fas fa-chart-line" style="color: violet; font-size:28px"></i></div>
                <div>Passport <i class="fas fa-passport" style="color: #445566; font-size:28px"></i></div>
            </div>
    </div>
</template>

<script>
export default {
    name: 'Simple_elements',
    data () {
            return {
            }
    }
}
</script>

<style>
</style>