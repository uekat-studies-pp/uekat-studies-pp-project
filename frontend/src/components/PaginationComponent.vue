<template>
  <div>
    <a v-for="(v, k) in pagination" v-bind:key="k" :href="calculateHref(v['page'])" @click.prevent="click"
      :data-page="v['page']" :class="v['active'] ? 'active' : ''">{{ v['page'] != null ? v['page'] : '...' }}</a>
  </div>
</template>

<script lang="ts">
interface PaginationItem {
  page: string;
  active: boolean;
}

export default {
  name: "PaginationComponent",
  props: {
    pagination: {
      required: true,
      type: Array as () => PaginationItem[],
    }
  },
  methods: {
    calculateHref(page: string) {
      if (page == "...") {
        return undefined;
      }

      const url = new URL(window.location.toString());
      url.searchParams.set('page', page);

      return url.toString();
    },
    click(e: any) {
      const criteria: { [key: string]: any } = {};
      if (e.currentTarget.dataset['page']) {
        criteria['page'] = e.currentTarget.dataset['page'];
      }

      this.$emit('updateListFromApi', criteria);
    }
  }
}
</script>

<style scoped></style>
