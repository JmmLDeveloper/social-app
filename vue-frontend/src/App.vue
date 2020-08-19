<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: "App",
  data() {
    return {
      msg: "hello world"
    };
  },
  mounted() {
    this.$store.dispatch("loadPosts");
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.form-group {
  display: flex;
  flex-direction: column;
  font-size: 2.2rem;
  align-items: flex-start;
  margin: 1rem 0;
}

.form-group label {
  margin-bottom: 0.5rem;
}

#login-view form {
  padding: 0 2rem 1.5rem;
}

input,
label,
button,
textarea {
  font-size: 1.4rem;
}

form input ,form textarea{
  width: 100%;
}

.actions {
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  width: 70%;
}

.actions p{
  margin: 0;
  margin-top: 0.5rem;
  font-size: 1.3rem;
}

form a {
  color: dodgerblue;
}
</style>
