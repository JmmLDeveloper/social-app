<template>
  <div>
    <Header />
    <form @submit.prevent="onSubmit">
      <h2>{{ action === "create" ? "Write Down Your Comment" :"Edit Your Previous Comment" }}</h2>
      <textarea v-model="content"></textarea>
      <button type="submit">Save</button>
    </form>
  </div>
</template>

<script>
import Header from "../components/Header";

export default {
  data() {
    let id = parseInt(this.$route.params.commentId);
    let comment = isNaN(id)
      ? null
      : this.$store.getters.getComment({
          postId: parseInt(this.$route.params.postId),
          commentId: id
        });
    return {
      content: (comment && comment.content) || "",
      action: isNaN(id) ? "create" : "edit"
    };
  },
  components: {
    Header
  },
  methods: {
    async onSubmit() {
      let comment = { content: this.content };
      let id = parseInt(this.$route.params.commentId);
      if (!isNaN(id)) comment.id = id;
      await this.$store.dispatch("storeComment", {
        comment,
        postId: this.$route.params.postId
        // dont check because a i am guaranteed that there will be post id
      });
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped>
form {
  width: 80%;
  margin: 0 auto;
}

form button {
  margin-top: 1rem;
}

h2 {
  margin-top: 3rem;
  font-size: 2rem;
}
</style>