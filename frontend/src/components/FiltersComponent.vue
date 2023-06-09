<template>
  <div class="column items-center q-mt-xl">
    <div style="width: 30vw" class="row justify-between">
      <q-input
          style="width: 20vw;"
          v-model="search_text"
          outlined
          label="Tytuł"
      />

      <q-option-group
          v-model="search_type"
          :options="[
              {
                label: 'Steam',
                value: 'steam'
              },
              {
                label: 'Gog',
                value: 'gog'
              },
            ]"
      />
    </div>

    <q-btn
      label="Wyszukaj"
      color="primary"
      @click="submit"
    />
  </div>
</template>

<script lang="ts">

import {ref, defineComponent} from "vue";

export default defineComponent({
  name: "FiltersComponent",
  emits: ['updateListFromApi'],
  setup(props, {emit}) {
    const search_text = ref('')
    const search_type = ref('steam')

    function submit() {
      emit('updateListFromApi', {t: search_text.value, type: search_type.value})
    }

    return {
      search_text,
      search_type,
      submit
    }
  }
})
</script>

<style scoped></style>
