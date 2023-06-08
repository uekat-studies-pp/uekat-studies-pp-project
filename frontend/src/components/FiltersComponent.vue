<template>
  <div>
    <form :action="action" :method="method">
      <div v-for="(element, key) in elements" v-bind:key="key">
        <input :type="element.type" :name="element.name" :value="element.value" />
      </div>
      <input type="submit" value="Submit" />
    </form>
  </div>
</template>

<script lang="ts">

export default {
  name: "FiltersComponent",
  data() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    return {
      action: "/api/list",
      method: "get",
      elements: [
        {
          type: "text",
          name: "t",
          value: urlParams.get('t'),
        },
        {
          type: "text",
          name: "type",
          value: urlParams.get('type'),
        }
      ]
    }
  }
}
</script>

<style scoped></style>
