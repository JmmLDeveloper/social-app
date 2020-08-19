<template>
  <div>
    <Header />
    <div>
      <h2>{{ action ==='create' ? 'Create New Post' : 'Edit Post'}}</h2>
      <form @submit.prevent="onSubmit">
        <div class="form-group">
          <label for="title-input">Title</label>
          <input type="text" v-model="title" id="title-input" />
        </div>
        <div class="form-group">
          <label for="content-input">Content</label>
          <textarea v-model="content" id="content-input" rows="5"></textarea>
        </div>
        <div class="form-group">
          <label for="tags-input">Tags</label>
          <select multiple v-model="tags" id="tags-input">
            <option v-for="t in optionTags" :key="t.id" :value="t.id">{{t.name}}</option>
          </select>
        </div>
        <button type="submit">{{ action === 'create' ? 'Create' : 'Edit'}}</button>
      </form>
    </div>
  </div>
</template>

<script>
import Header from "../components/Header";

export default {
  components: {
    Header
  },
  data() {
    let id = parseInt(this.$route.params.id);
    let post = isNaN(id) ? null : this.$store.getters.getPost(id);
    return {
      action: post ? "edit" : "create",
      title: (post && post.title) || "",
      content: (post && post.content) || "",
      tags: (post && post.tags.map(t => t.id)) || [],
      formSubmitted: false
    };
  },
  methods: {
    async onSubmit() {
      let { title, content, tags } = this;
      let newPost = { title, content, tags };
      let id = parseInt(this.$route.params.id);
      if (!isNaN(id)) newPost.id = id;
      await this.$store.dispatch("storePost", newPost);
      this.$router.push("/posts/");
    }
  },
  computed: {
    optionTags() {
      return this.$store.getters.getTags;
    }
  },
  async mounted() {
    if (!this.$store.getters.tagsAreLoaded)
      await this.$store.dispatch("loadTags");
  },
  watch: {
    $route(to) {
      if (to.fullPath === "/create-post") {
        this.title = "";
        this.content = "";
        this.tags = [];
        this.action = "create";
      }
    }
  }
};
</script>

<style scoped>
h2 {
  margin-top: 3rem;
  font-size: 2.1rem;
}

.success {
  font-size: 3rem;
  color: green;
}

form {
  margin: 0 auto;
  width: 70%;
}
</style>
