<template>
  <div id="login-view">
    <div id="wrapper">
      <main>
        <header>
          <h1>Login</h1>
        </header>
        <form @submit.prevent="onSubmit">
          <div class="form-group">
            <label for="username-input">Username</label>
            <input type="text" v-model="username" id="username-input" />
          </div>
          <div class="form-group">
            <label for="password-input">Password</label>
            <input type="password" v-model="password" id="password-input" />
          </div>
          <div class="actions">
            <button type="submit">Send</button>
            <p>
              or
              <router-link to="/registration">registrer</router-link>,if you don't have an account
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
      password: ""
    };
  },
  methods: {
    async onSubmit() {
      let { username, password } = this;
      let res;
      try {
        res = await fetch("http://localhost:8000/api/login/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password })
        });
      } catch (err) {
        console.log('could not connet to http://localhost:8000/api/login/"')
        alert('errors on console')
        return;
      }

      if (res.ok) {
        let token = (await res.json()).token;
        await this.$store.dispatch("auth", { token });
        this.$router.push("/posts/");
      } else {
        let errors = await res.text();
        console.log(errors);
        alert('errors on console')
      }
    }
  }
};
</script>

<style>
#login-view {
  height: 100vh;
  position: relative;
  widows: 100vw;
  padding: 0.5rem;
  background-color: #efefef;
}

#login-view #wrapper {
  position: absolute;
  top: 20%;
  left: 0;
  right: 0;
}

#login-view main {
  display: inline-block;
  margin: 0 auto;
  border: solid 1px grey;
  background-color: white;
}

#login-view header h1 {
  color: white;
  margin: 0;
  font-size: 2rem;
}

#login-view header {
  padding: 1rem 0;
  background-color: #48c9b0;
}
</style>
