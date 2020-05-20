
Vue.component("app-header", {
  template: `
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <a class="navbar-brand" href="#">Lab 7</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <router-link class="nav-link" to="/">Home <span class="sr-only">(current)</span></router-link>
          </li>
          <li class="nav-item">
          <a class="nav-link" href=""
            >Explore <span class="sr-only">(current)</span></a
          >
        </li>
        <li class="nav-item">
          <a class="nav-link" href=""
            >My Profile <span class="sr-only">(current)</span></a
          >
        </li>
        <li class="nav-item">
          <a class="nav-link" href=""
            >Logout <span class="sr-only">(current)</span></a
          >
        </li>
        </ul>
      </div>
    </nav>
    `,
});

const Home = Vue.component("home", {
  template: `
  <div class="logingrid">
  <div class="loginimage">
    <img src="/static/images/karl-lee-ojb8uwDDXu8-unsplash.jpg"/>
  </div>
  <div class="loginbox">
    <h2>Photogram</h2>
    <router-link to="/register" tag="button">Register</router-link>
    <router-link to="/login" tag="button">Login</router-link>
  </div>
  </div>
   `,
  data: function () {
    return {};
  },
});



const Register = Vue.component("register-form", {
   methods: {
            async  get() { 
         const res = await fetch('/api/users');
  				const data = await res.json();
          //alert(JSON. stringify(data));
              },
              
            async post() {
      let headers = {
    'Content-Type': 'application/json'
  };
       var obj =  {
    biography: "Dolor et aute non officia laborum aliquip dolor fugiat sunt culpa cupidatat. Consectetur id laboris excepteur voluptate voluptate consectetur elit eu ullamco laboris irure commodo culpa exercitation. Ex id laborum ad dolor aliqua veniam veniam.\r\n", 
    email: "jillianbeasley@papricut.com", 
    first_name: "Gallegos", 
    last_name: "Bailey", 
    location: "Drummond", 
    password: "Beasley", 
    photo: "http://placehold.it/32x32", 
    username: "Jillian"
  };
      	const request = new Request(
        		'/api/users/register',
        {
          method: "POST",
          headers,
          body: JSON.stringify(obj)

        },

      );
        const res = await fetch(request);
        const data = await res.json();
        this.data = data;
        alert(JSON. stringify(data));
            
              
            }     

        } ,

        

  template: 

  ` 
  <div>
  <input v-model="username" placeholder="username">
  <br>
  <input v-model="fname" placeholder="fname">
  <br>
  <input v-model="lname" placeholder="lname">
  <br>
  <input v-model="password" placeholder="password">
  <br>
  <input v-model="biography" placeholder="biography">
  <br>
    <input v-model="gender" placeholder="gender">
  <br>

      <input v-model="email" placeholder="email">
  <br>
      <input v-model="photo" placeholder="photo">
  <br>

  <button v-on:click="post">Register</button>  
  </div>
`
});

const Login = Vue.component("login-form", {
  template: `
    <div>
  <h4>Login</h4>
  <form
  v-on:submit.prevent=""
  method="POST"
  action="/api/auth/login"
  enctype="multipart/form-data"
  id="loginForm"
  >
  <div class="myform">
    <div class="section">
      <label>Username</label>
      <input type="text" name="username" />
    </div>
    <div class="section">
      <label>Password</label>
      <input type="password" name="password" />
    </div>
    </div>
    <div class="section"><button type="submit">Login</button></div>
</form>
</div>
   `,
  data: function () {
    return {};
  },
});

const NotFound = Vue.component("not-found", {
  template: `
    <div>
        <h1>404 - Not Found</h1>
    </div>
    `,
  data: function () {
    return {};
  },
});

// Define Routes
const router = new VueRouter({
  mode: "history",
  routes: [
    { path: "/", component: Home },
    // Put other routes here
    { path: "/register", component: Register },
    { path: "/login", component: Login },
    // This is a catch all route in case none of the above matches
    { path: "*", component: NotFound },
  ],
});

// Instantiate our main Vue Instance
let app = new Vue({
  el: "#app",
  router,
});
