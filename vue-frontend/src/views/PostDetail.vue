<template>
  <div>
    <Header />
    <div id="post-detail">
      <header>
        <div id="header-top">
          <h2>{{post.title}}</h2>
          <div class="btns" v-if="post.author === user.username">
            <button @click="$router.push(`/posts/${post.id}/edit`)" class="ic-btn edit-btn">
              <span class="material-icons">create</span>
            </button>
            <button @click="onDeleteClick" class="ic-btn delete-btn">
              <span class="material-icons">delete</span>
            </button>
          </div>
        </div>

        <div id="meta-data">
          <span>posted at</span>
          <span class="published_date">{{ post.published_date }}</span>
          <span>by</span>
          <span class="author"> <UserTag :username="post.author" /></span>
        </div>
        <div id="tags">
          <ul id="tag-list">
            <li :key="tag.id" v-for="tag in post.tags">{{tag.name}}</li>
          </ul>
        </div>
      </header>
      <main>
        <p id="content">{{post.content}}</p>
        <h3>Comments</h3>
        <ul>
          <li v-for="c in post.comments" :key="c.id">
            <Comment :comment="c" :username="user.username" :postId="post.id" />
          </li>
        </ul>
        <div id="create-comment-link">
          <router-link :to="`/posts/${post.id}/comments/create`">Write Comment</router-link>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import Header from "../components/Header";
import Comment from "../components/Comment";
import UserTag from "../components/UserTag"
export default {
  data() {
    return {
      id: null
    };
  },
  created() {
    //hize esto por que vue me retorna un valor raro y
    //nececito un exactamente un numero para la comparacion
    this.id = parseInt(this.$route.params.id);
  },
  mounted() {
    if (!this.post.comments) this.$store.dispatch("loadPostComments", this.id);
  },
  computed: {
    post() {
      let post = this.$store.getters.getPost(this.id);
      if (!post) return {}; // preventing : post.content does not exist
      if (!post.content) this.$store.dispatch("loadPostContent", this.id);
      return post || {};
    },
    user() {
      return this.$store.getters.getUser;
    }
  },
  components: {
    Header,
    Comment,
    UserTag,
  },
  methods: {
    async onDeleteClick() {
      await this.$store.dispatch("deletePost", this.post.id);
      this.$router.push("/posts/");
    }
  }
};
</script>

<style scoped>
.btns {
  display: flex;
  margin-left: 1rem;
}

#create-comment-link a {
  display: inline-block;
  background: rgb(64, 224, 91);
  border-radius: 0.2rem;
  padding: 0.5rem 0.5rem;
  color: white;
  font-size: 1.4rem;
  text-decoration: none;
}

#create-comment-link {
  margin-top: 1rem;
  padding: 0.5rem 0;
}

#header-top {
  display: flex;
  align-items: center;
}

.ic-btn {
  margin: 0 0.2rem;
  padding: 0.2rem;
  display: flex;
  color: white;
  justify-content: center;
  align-items: center;
}

.delete-btn {
  background-color: tomato;
}

.edit-btn {
  background-color: rgb(221, 218, 55);
}

#post-detail {
  width: 90%;
  margin: 2rem auto;
}

#post-detail #content {
  font-size: 1.2rem;
}

#post-detail h2 {
  font-size: 2.3rem;
  display: inline;
  margin: 0;
  text-align: start;
}

#post-detail h3 {
  font-size: 2rem;
  margin: 0;
  text-align: start;
}

#post-detail header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-bottom: 0.5rem;
  border-bottom: solid 2px grey;
}

#post-detail .published_date {
  font-size: 1em;
  font-weight: bold;
  color: grey;
}

#post-detail .author {
  font-size: 1.2em;
  color: green;
}

#tag-list {
  display: flex;
  margin: 0.3rem 0;
}

#meta-data
{
  display: flex;
  align-items: baseline;
}

#meta-data span
{
  margin: 0 0.2rem;
}

#tag-list li {
  font-size: 0.9rem;
  font-weight: bolder;
  margin-right: 0.3rem;
  border-radius: 0.2rem;
  background-color: rgb(212, 208, 147);
  padding: 0.2rem 0.6rem;
}
</style>