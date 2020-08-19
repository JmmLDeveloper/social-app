<template>
  <ul id="post-list">
    <li :key="post.id" v-for="post in posts">
      <PostPreview :post="post" />
    </li>
  </ul>
</template>

<script>
import PostPreview from './PostPreview'

export default {
  props: ["posts"],
  components: {
    PostPreview
  }
};
</script>

<style scoped>
#post-list {
  width: 80%;
  margin: 0 auto;
}
</style>
