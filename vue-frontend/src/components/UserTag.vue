<template>
  <span @click="onClick" class="user-tag">
    {{username}}
    <span class="is-sub" v-if="isSub">
      sub
    </span>
  </span>
</template>

<script>
export default {
  props: ["username"],
  computed: {
    isSub() {
      return this.$store.getters.isSub(this.$props.username);
    }
  },
  methods: {
    onClick() {
      if (this.$store.getters.isSub(this.$props.username)) {
        if (confirm("wanna unsubscribe ?"))
          this.$store.dispatch("unsubscribeUser", this.$props.username);
      } else {
        if (confirm("wanna subscribe ?"))
          this.$store.dispatch("subscribeUser", this.$props.username);
      }
    }
  }
};
</script>

<style scoped>
.user-tag {
  display: inline-flex;
  color: green;
  align-items: flex-end;
  font-weight: bolder;
  cursor: pointer;
}

.user-tag:hover {
  color: rgb(61, 202, 61);
}

.is-sub {
  color:grey;
  display: block;
  transform: scaleY(0.9);
  margin-left: 0.3rem;
  font-size: 0.8rem;
}
</style>