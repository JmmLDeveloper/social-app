<template>
  <div class="post">
    <header>
      <div class="meta-data">
        <router-link :to="`/posts/${post.id}`">
          <span class="title">{{ post.title }}</span>
        </router-link>
        <div style="font-size:0.9rem">
          <span> posted at </span>
          <span class="published_date">{{ post.published_date }}</span>
          <span> by </span>
          <span class="author"> <UserTag :username="post.author" /></span>

        </div>
      </div>
      <div>
        <button @click="toggleExpanded">{{ expanded ? 'hide' : 'expand' }}</button>
      </div>
    </header>
    <main class="content" v-if="post.content && expanded">{{post.content}}</main>
  </div>
</template>

<script>
import UserTag from '../components/UserTag'

export default {
  props: ["post"],
  data() {
    return {
      expanded: false
    };
  },
  methods: {
    toggleExpanded() {
      let post = this.$props.post;
      if (!post.content) this.$store.dispatch("loadPostContent", post.id);
      this.expanded = !this.expanded;
    }
  },
  components : {
    UserTag
  }
};
</script>

<style scoped>
a {
  text-decoration: none;
  color: rgb(14, 104, 69);
}

a:hover {
  color: rgb(26, 180, 26);
}

.post {
  margin: 1.1rem 0;
  padding: 0.5rem;
  border: solid 1px grey;
  background: rgb(197, 226, 197);
}

.post header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.post .title {
  font-size: 1.5rem;
}

.post .published_date {
  font-size: 0.8em;
  font-weight: bold;
  color: grey;
}

.post .author {
  font-size: 1em;
  color: green;
}

.post .meta-data {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.post .content {
  text-align: le;
  border-top: solid grey 1px;
  padding: 1rem 0.5rem;
}
</style>
