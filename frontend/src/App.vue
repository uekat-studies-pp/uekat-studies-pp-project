<template>
  <div>
    <FiltersComponent @updateListFromApi="updateListFromApi"/>
    <ContentComponent :list="list"/>
    <PaginationComponent :pagination="pagination" @updateListFromApi="updateListFromApi"/>
  </div>
</template>

<script lang="ts">
import FiltersComponent from './components/FiltersComponent.vue'
import ContentComponent from './components/ContentComponent.vue'
import PaginationComponent from './components/PaginationComponent.vue'

export default {
  name: "App",
  components: {
    FiltersComponent,
    ContentComponent,
    PaginationComponent
  },
  data() {
    return {
      list: [],
      pagination: []
    }
  },
  created() {
    this.updateListFromApi()
  },
  methods: {
    updateListFromApi(criteria = {}) {
      const self = this;
      const url = new URL(window.location);
      url.pathname = "/api/list";

      for (const [key, value] of Object.entries(criteria)) {
        url.searchParams.set(key, value);
      }

      fetch(url.toString()).then(response => response.json()).then(data => {
        self.list = data.list;
        self.pagination = data.pagination;
      })
    }
  }
}
</script>

<style scoped></style>
