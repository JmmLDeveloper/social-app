<template>
  <header>
    <div class="header-left">
      <h1>Social App</h1>
      <p>welcome again, {{ username }}</p>
    </div>
    <nav>
      <ul>
        <li>
          <router-link to="/posts">Feed</router-link>
          <router-link to="/filters">Filters</router-link>
          <router-link to="/create-post">Create Post</router-link>
          <router-link to="/login">Login</router-link>
          <router-link to="/registration">Registration</router-link>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script>
export default {
  computed: {
    username() {
      return this.$store.getters.getUser.username;
    }
  }
};
</script>

<style scoped>
header 
{
  background-color: #48c9b0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
}

header h1 ,header p
{
  margin:0;
}

.header-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.header-right {

}

header a
{
  color: rgb(236, 228, 218);
  margin: 0 0.6rem;
  text-decoration: none;
  font-size: 1.5rem;
}

header a:hover
{
  color: white;
}


</style>