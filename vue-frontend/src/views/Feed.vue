<template>
  <div>
    <Header />
    <h2>Post List</h2>
    <PostList :posts="posts" />
  </div>
</template>

<script>
import Header from "../components/Header";
import PostList from "../components/PostList";

export default {
  components: {
    Header,
    PostList
  },
  computed: {
    posts() {
      return this.$store.getters.getPosts;
    }
  }
};
</script>

<style scoped>
h2 {
  margin-top: 2.5rem;
  font-size: 2.5rem;
}
</style>