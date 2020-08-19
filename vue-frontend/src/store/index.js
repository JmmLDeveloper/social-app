import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const BACKEND_URL = "http://localhost:8000/api";

export default new Vuex.Store({
  state: {
    token: null,
    user: null,
    tags: [],
    tagsAreLoaded: false,
    posts: [],
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
    },
    setUser(state, user) {
      state.user = user;
    },
    setTags(state, tags) {
      state.tagsAreLoaded = true;
      state.tags = tags;
    },
    setPosts(state, posts) {
      state.posts = posts;
    },
    setPostContent(state, { id, content }) {
      state.posts = state.posts.map((post) =>
        post.id !== id ? post : { ...post, content: content }
      );
    },
    setPostComments(state, { id, comments }) {
      state.posts = state.posts.map((post) =>
        post.id !== id ? post : { ...post, comments: comments }
      );
    },
    deletePost(state, id) {
      state.posts = state.posts.filter((p) => p.id !== id);
    },
    addPost(state, newPost) {
      state.posts = [...state.posts, newPost];
    },
    editPost(state, { newPost, id }) {
      state.posts = state.posts.map((p) => (p.id === id ? newPost : p));
    },
    addComment(state, { postId, newComment }) {
      state.posts = state.posts.map((post) => {
        if (post.id == postId) {
          let newComments = [...post.comments, newComment];
          return { ...post, comments: newComments };
        } else return post;
      });
    },
    editComment(state, { postId, commentId, newComment }) {
      state.posts = state.posts.map((post) => {
        if (post.id == postId) {
          let newComments = post.comments.map((c) => {
            if (c.id === commentId) return newComment;
            else return c;
          });
          return { ...post, comments: newComments };
        } else return post;
      });
    },
    deleteComment(state, { postId, commentId }) {
      state.posts = state.posts.map((post) => {
        if (post.id === postId) {
          let newComments = post.comments.filter((c) => c.id !== commentId);
          return { ...post, comments: newComments };
        } else return post;
      });
    },
    addSub(state, username) {
      state.user = {
        ...state.user,
        subscription_users: [...state.user.subscription_users, username],
      };
    },
    deleteSub(state, username) {
      state.user = {
        ...state.user,
        subscription_users: state.user.subscription_users.filter(
          (u) => u != username
        ),
      };
    },
  },
  actions: {
    async subscribeUser({ commit, state }, targetUsername) {
      let res = await fetch(`${BACKEND_URL}/subscription/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${state.token}`,
        },
        body: JSON.stringify({ "target-username": targetUsername }),
      });
      if (res.ok) commit("addSub", targetUsername);
    },
    async unsubscribeUser({ commit, state }, targetUsername) {
      let res = await fetch(`${BACKEND_URL}/subscription/`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${state.token}`,
        },
        body: JSON.stringify({ "target-username": targetUsername }),
      });
      if (res.ok) commit("deleteSub", targetUsername);
    },
    //save or update
    //in the two requests URLs a need to set expand=tags
    //in order the get the tags name of the post and
    //properly display the tags of the added post
    async storeComment({ commit, state }, { comment, postId }) {
      if (comment.id) {
        let res = await fetch(
          `${BACKEND_URL}/posts/${postId}/comments/${comment.id}/`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${state.token}`,
            },
            body: JSON.stringify(comment),
          }
        );
        let newComment = await res.json();
        commit("editComment", {
          newComment,
          commentId: comment.id,
          postId,
        });
      } else {
        let res = await fetch(`${BACKEND_URL}/posts/${postId}/comments/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${state.token}`,
          },
          body: JSON.stringify(comment),
        });
        let newComment = await res.json();
        commit("addComment", {
          newComment,
          postId,
        });
      }
    },
    async storePost({ commit, state }, post) {
      if (post.id) {
        let res = await fetch(`${BACKEND_URL}/posts/${post.id}/?expand=tags`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${state.token}`,
          },
          body: JSON.stringify(post),
        });
        let newPost = await res.json();
        commit("editPost", {
          newPost,
          id: post.id,
        });
      } else {
        let res = await fetch(`${BACKEND_URL}/posts/?expand=tags`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${state.token}`,
          },
          body: JSON.stringify(post),
        });
        let newPost = await res.json();
        commit("addPost", newPost);
      }
    },
    async auth({ commit }, payload) {
      commit("setToken", payload.token);
      let res = await fetch(`${BACKEND_URL}/user/`, {
        headers: { Authorization: `Bearer ${payload.token}` },
      });
      let userData = await res.json();
      commit("setUser", userData);
    },
    async loadTags({ commit }) {
      let res = await fetch(`${BACKEND_URL}/tags/`);
      let tags = await res.json();
      commit("setTags", tags);
    },
    async loadPosts({ commit }) {
      let res = await fetch(`${BACKEND_URL}/posts/?omit=content&expand=tags`);
      let posts = await res.json();
      commit("setPosts", posts);
    },
    async loadPostContent({ commit }, id) {
      let res = await fetch(`${BACKEND_URL}/posts/${id}/?fields=content`);
      let content = (await res.json()).content;
      commit("setPostContent", { id, content });
    },
    async loadPostComments({ commit }, id) {
      let res = await fetch(`${BACKEND_URL}/posts/${id}/comments/`);
      let comments = await res.json();
      commit("setPostComments", { id, comments });
    },
    async deletePost({ commit, state }, id) {
      let token = state.token;
      let res = await fetch(`${BACKEND_URL}/posts/${id}/`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) commit("deletePost", id);
    },
    async deleteComment({ commit, state }, { commentId, postId }) {
      let token = state.token;
      let res = await fetch(
        `${BACKEND_URL}/posts/${postId}/comments/${commentId}`,
        {
          method: "DELETE",
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (res.ok) commit("deleteComment", { commentId, postId });
    },
    async applyFilters({ commit, state }, { tags, subs_only }) {
      let urlSP = new URLSearchParams();
      for (let tag of tags) {
        urlSP.append("tags", tag);
      }
      if (subs_only) 
        urlSP.set("subs_only", "1");
      let queryString = urlSP.toString();

      let res = await fetch(
        `${BACKEND_URL}/posts/?omit=content&expand=tags&${queryString}`,
        {
          headers: { Authorization: `Bearer ${state.token}` },
        }
      );
      let posts = await res.json();
      commit("setPosts", posts);
    },
  },
  getters: {
    getToken(state) {
      return state.token;
    },
    getUser(state) {
      return state.user;
    },
    tagAreLoaded(state) {
      return state.tagsAreLoaded;
    },
    getTags(state) {
      return state.tags;
    },
    getPosts(state) {
      return state.posts;
    },
    getPost: (state) => (id) => {
      return state.posts.find((post) => post.id === id);
    },
    getComment: (state) => ({ postId, commentId }) => {
      let post = state.posts.find((post) => post.id === postId);
      return post.comments.find((c) => c.id === commentId);
    },
    isSub: (state) => (username) => {
      return state.user.subscription_users.includes(username);
    },
  },
});
