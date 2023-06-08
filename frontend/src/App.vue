<template>
  <div>
    <FiltersComponent />
    <ContentComponent :list="list" />
  </div>
</template>

<script lang="ts">
import FiltersComponent from './components/FiltersComponent.vue'
import ContentComponent from './components/ContentComponent.vue'

export default {
  name: "App",
  components: {
    FiltersComponent,
    ContentComponent
  },
  data() {
    return {
      list: []
    }
  },
  created() {
    this.updateListFromApi()
  },
  methods: {
    updateListFromApi(criteria = {}) {
      const self = this;
      const url = new URL(window.location);

      if ('action' in criteria && criteria['action']) {
        url.pathname = criteria['action'];
        delete criteria['action'];
      } else {
        url.pathname = "/api/list";
      }

      for (const key in criteria) {
        if (Object.prototype.hasOwnProperty.call(criteria, key)) {
          const value = criteria[key];
          url.searchParams.set(key, value);
        }
      }

      fetch(url.toString()).then(response => response.json()).then(data => {
        console.log(data);
      })
    }
  }
}
</script>

<style scoped></style>
