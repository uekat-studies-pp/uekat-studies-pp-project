<template>
  <div>
    <a v-for="(v, k) in pagination" v-bind:key="k" :href="calculateHref(v['page'])" @click.prevent="click" :data-page="v['page']">{{ v['page'] != null ? v['page'] : '...' }}</a>
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
    },
    click(e) {
      const criteria = {};
      if (e.currentTarget.dataset['page']) {
        criteria['page'] = e.currentTarget.dataset['page'];
      }

      this.$emit('updateListFromApi', criteria);
    }
  }
}
</script>

<style scoped></style>
