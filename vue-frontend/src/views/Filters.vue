<template>
  <div>
    <Header />
    <main>
      <h2>Filters</h2>
      <div class="row checkbox">
        <label for="onlysub-input">Only Show Posts of your subscriptions</label>
        <input type="checkbox" v-model="subs_only" id="onlysub-input" />
      </div>
      <div class="row">
        <label for="tags-input">Show Posts With These Tags</label>
        <select multiple v-model="tags" id="tags-input">
          <option v-for="t in optionTags" :key="t.id" :value="t.id">{{t.name}}</option>
        </select>
      </div>
      <button @click="apply">Apply Filters ( re-request )</button>
    </main>
  </div>
</template>

<script>
import Header from "../components/Header";
export default {
  data() {
    return {
      tags: [],
      subs_only: false
    };
  },
  async mounted() {
    if (!this.$store.getters.tagsAreLoaded)
      await this.$store.dispatch("loadTags");
  },
  methods: {
    async apply() {
      let { tags, subs_only } = this;
      await this.$store.dispatch("applyFilters", { tags, subs_only });
      this.$router.push("/posts/");
    }
  },
  computed: {
    optionTags() {
      return this.$store.getters.getTags;
    }
  },
  components: {
    Header
  }
};
</script>

<style scoped>
h2 {
  margin-top: 2rem;
  font-size: 2.3rem;
}

main {
  width: 80%;
  margin: 0 auto;
}

.row.checkbox {
  align-items: center;
}

.row {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  margin: 2rem 0rem;
}

.row input,
.row select {
  margin-left: 1rem;
}
</style>