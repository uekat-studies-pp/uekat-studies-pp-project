<template>
  <div>
    <form :action="action" :method="method" @submit.prevent="submit">
      <div v-for="(element, key) in elements" v-bind:key="key">
        <div v-if="element.type == 'select'">
          <label :for="element.id">{{ element.label }}</label>
          <select :id="element.id" :name="element.name">
            <option v-for="(v, k) in element.options" v-bind:key="k" :value="k"
              :selected="urlParamHasKeyValue(element.name, k) ? true : false">
              {{ v }}
            </option>
          </select>
        </div>
        <div v-else>
          <label :for="element.id">{{ element.label }}</label>
          <input :type="element.type" :id="element.id" :name="element.name" :value="element.value" />
        </div>
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
      urlParams: urlParams,
      action: "/",
      method: "get",
      elements: [
        {
          type: "text",
          id: "t",
          name: "t",
          value: urlParams.get('t'),
          label: "Tytuł",
        },
        {
          type: "select",
          id: "type",
          name: "type",
          value: urlParams.get('type'),
          label: "Typ",
          options: {
            'steam': "Steam",
            'gog': "Gog",
          }
        }
      ]
    }
  },
  methods: {
    urlParamHasKeyValue(key: string, value: string) {
      return this.urlParams.get(key) == value
    },
    submit(e: any) {
      let criteria: { [key: string]: any } = {};
      const formData = new FormData(e.currentTarget);

      this.setCriteriaFromCurrentUrl(criteria);

      criteria['page'] = 1;

      if (formData.has('t')) {
        criteria['t'] = formData.get('t');
      }

      if (formData.has('type')) {
        criteria['type'] = formData.get('type');
      }

      this.$emit('updateListFromApi', criteria);
    },
    setCriteriaFromCurrentUrl(criteria: { [key: string]: any }) {
      const url = new URL(window.location.toString());
      url.searchParams.forEach((value, key) => {
        criteria[key] = value;
      });
    }
  }
}
</script>

<style scoped></style>
