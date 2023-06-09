<template>
  <div class="row justify-center q-my-xl">
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
  </div>
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
      type: Array,
    }
  }
}
</script>

<style scoped></style>
