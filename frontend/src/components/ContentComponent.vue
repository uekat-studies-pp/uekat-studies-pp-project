<template>
  <table>
    <thead>
      <tr>
        <th>Tytuł</th>
        <th>Typ</th>
        <th>Cena</th>
        <th>Cena po promocji</th>
        <th>Link</th>
      </tr>
    </thead>
    <tbody>
      <ContentItemComponent v-for="(item, key) in list" v-bind:key="key" :item="item"></ContentItemComponent>
    </tbody>
  </table>
</template>

<script lang="ts">
import ContentItemComponent from './ContentItemComponent.vue';

export default {
  name: "ContentComponent",
  components: {
    ContentItemComponent,
  },
  props: {
    list: {
      required: true,
      type: Array<Object>,
    }
  }
}
</script>

<style scoped></style>
