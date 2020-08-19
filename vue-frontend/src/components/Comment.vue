<template>
  <div class="comment">
    <header>
      <div class="comment-data">
        <span class="title"> <UserTag :username="comment.author" /> </span>
        <span class="published_date">{{ comment.published_date }}</span>
      </div>
      <div v-if="username === comment.author">
        <button
          @click="$router.push(`/posts/${postId}/comments/${comment.id}/edit`)"
          class="ic-btn edit-btn"
        >
          <span class="material-icons">create</span>
        </button>
        <button @click="onDeleteClick" class="ic-btn delete-btn">
          <span class="material-icons">delete</span>
        </button>
      </div>
    </header>

    <p class="content">{{ comment.content }}</p>
  </div>
</template>

<script>

import UserTag from '../components/UserTag'

export default {
  props: ["comment", "postId", "username"],
  methods: {
    onDeleteClick() {
      if (confirm("are you sure you want to delete this comment?"))
        this.$store.dispatch("deleteComment", {
          commentId: parseInt(this.$props.comment.id),
          postId: parseInt(this.$props.postId)
        });
    }
  },
  components : {
    UserTag
  }
};
</script>

<style scoped>
.ic-btn {
  background-color: transparent;
  border: none;
  outline: none;
  padding: 0;
  margin: 0 0.4rem;
  cursor: pointer;
}

.delete-btn {
  color: rgb(255, 86, 71);
}

.edit-btn {
  color: rgb(140, 175, 26);
}

.ic-btn span {
  font-size: 1.2rem;
}

.comment {
  margin: 1rem 0.5rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-bottom: 1rem;
  border-bottom: solid 2px grey;
}

.comment-data {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.comment header {
  display: flex;
  width: 100%;
  align-items: flex-start;
  justify-content: space-between;
}

.comment .content {
  font-size: 1.2rem;
  margin: 0.2rem 0 0;
}

.comment .published_date {
  font-size: 0.9em;
  font-weight: bold;
  color: grey;
}

.comment .author {
  font-size: 1em;
}
</style>