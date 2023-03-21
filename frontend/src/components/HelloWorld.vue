<template>
  <div class="column items-center">
    <h1>{{ msg }}</h1>

    <q-card class="card_style bg-teal text-center">
      <q-card-section>
        Count: {{ count }}
        Double count: {{ doubleCount }}
      </q-card-section>

      <q-card-section>
        <q-btn
            @click="increment"
            label="Increment"
        />
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup lang="ts">
import {useCounterStore} from "../store/counter";
import { storeToRefs } from 'pinia'

defineProps({
  msg: String
})

const store = useCounterStore()

const { count, doubleCount } = storeToRefs(store)
const { increment } = store
</script>

<style scoped>
.card_style {
  width: 50vw;
  height: 50vh
}
</style>
