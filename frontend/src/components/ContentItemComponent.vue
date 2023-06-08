<template>
  <tr>
    <td> {{ item.title }} </td>
    <td> {{ item.type }} </td>
    <td> {{ item.price }} </td>
    <td> {{ item.priceafterdiscount !== null ? item.priceafterdiscount : '-' }} </td>
    <td> <a :href="item.url" target="_blank">Link</a> </td>
  </tr>
</template>

<script lang="ts">

export default {
  name: "ContentItemComponent",
  props: {
    item: {
      required: true,
      type: Object,
    }
  }
}
</script>

<style scoped></style>
