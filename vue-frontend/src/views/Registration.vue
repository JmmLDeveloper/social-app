<template>
  <div id="registration-view">
    <div id="wrapper">
      <main>
        <header>
          <h1>Registration</h1>
        </header>
        <form @submit.prevent="onSubmit">
          <div id="first-row">
            <label for="username-input">Username</label>
            <input type="text" v-model="username" id="username-input" />
            <label for="first_name-input">First Name</label>
            <input type="text" v-model="first_name" id="first_name-input" />
            <label for="age-input">Age</label>
            <input type="number" v-model="age" id="age-input" />
          </div>
          <div class="form-group">
            <label for="description-input">Description of yourself</label>
            <textarea v-model="description" rows="5" id="description-input"></textarea>
          </div>
          <div id="password-row">
            <label for="password1-input">Password</label>
            <input type="password" v-model="password1" id="password1-input" />
            <label for="password2-input">Confirm Password</label>
            <input type="password" v-model="password2" id="password2-input" />
          </div>
          <div class="actions">
            <button id="register-button" type="submit">Send</button>
            <p>
              or
              <router-link to="/login">Log In</router-link>,if you already have an account
            </p>
          </div>
        </form>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password1: "",
      password2: "",
      first_name: "",
      age: "",
      description: ""
    };
  },
  methods: {
    async onSubmit() {
      let {
        username,
        first_name,
        password1,
        password2,
        age,
        description
      } = this;
      let res;
      try {
        res = await fetch("http://localhost:8000/api/register/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username,
            password1,
            password2,
            age,
            description,
            first_name
          })
        });
      } catch (err) {
        alert("errores en consola");
        console.log("could not connet to http://localhost:8000/api/register/");
        return;
      }

      if (res.ok) {
        let token = (await res.json()).token;
        await this.$store.dispatch("auth", { token });
        this.$router.push("/posts/");
      } else {
        let errors = await res.json();
        console.log(errors);
        alert("errors on console");
      }
    }
  }
};
</script>

<style>
#registration-view {
  height: 100vh;
  position: relative;
  widows: 100vw;
  padding: 0.5rem;
  background-color: #efefef;
}

#registration-view #wrapper {
  position: absolute;
  top: 10%;
  left: 0;
  right: 0;
}

#registration-view main {
  width: 70%;
  margin: 0 auto;
  border: solid 1px grey;
  background-color: white;
}

#registration-view form {
  padding: 1.5rem 2rem;
}

#registration-view header h1 {
  color: white;
  margin: 0;
  font-size: 2rem;
}

#registration-view header {
  padding: 1rem 0;
  background-color: #48c9b0;
}

#first-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

#first-row input,
#password-row input {
  width: 20%;
}

#first-row,
#password-row {
  margin-bottom: 1rem;
}

#password-row {
  display: flex;
  justify-content: space-around;
}

#register-button {
  font-size: 1.5rem;
  margin: 0 auto;
  padding: 0.3rem 2rem;
}
</style>
