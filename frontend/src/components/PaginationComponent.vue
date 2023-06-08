<template>
  <div>
    <a v-for="(v, k) in pagination" v-bind:key="k" :href="calculateHref(v['page'])">{{ v['page'] }}</a>
  </div>
</template>

<script lang="ts">
export default {
  name: "PaginationComponent",
  props: {
    pagination: {
      required: true,
      type: Array,
    }
  },
  methods: {
    calculateHref(page) {
      if (page == "...") {
        return false;
      }

      const url = new URL(window.location);
      url.searchParams.set('page', page);

      return url.toString();
    }
  }
}
</script>

<style scoped></style>
