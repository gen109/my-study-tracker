<template>
  <div>
    <div class="check-node" :style="{ paddingLeft: `${depth * 20}px` }">
      <label class="check-label">
        <input
          type="checkbox"
          :checked="selectedIds.has(node.master_id)"
          @change="$emit('toggle', node.master_id)"
        />
        <span class="node-icon" v-if="depth > 0">└</span>
        <span class="node-name">{{ node.name }}</span>
      </label>
    </div>
    <MasterCheckNode
      v-for="child in node.children"
      :key="child.master_id"
      :node="child"
      :depth="depth + 1"
      :selected-ids="selectedIds"
      @toggle="$emit('toggle', $event)"
    />
  </div>
</template>

<script setup lang="ts">
import type { MasterCategory } from '@/stores/master'

defineProps<{
  node: MasterCategory
  depth: number
  selectedIds: Set<string>
}>()

defineEmits<{
  (e: 'toggle', masterId: string): void
}>()
</script>

<style scoped>
.check-node {
  padding: 0.3rem 0;
}

.check-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
  color: #2c3e50;
  font-weight: normal;
}

.check-label input[type='checkbox'] {
  cursor: pointer;
  width: 15px;
  height: 15px;
}

.node-icon { color: #bdc3c7; font-size: 0.8rem; }
.node-name { flex: 1; }
</style>
