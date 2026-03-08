<template>
  <div>
    <div class="master-node" :style="{ paddingLeft: `${depth * 20}px` }">
      <span class="node-icon" v-if="depth > 0">└</span>
      <span class="node-name">{{ node.name }}</span>
      <button class="delete-btn" @click="$emit('delete', node.master_id)">✕</button>
    </div>
    <MasterNode
      v-for="child in node.children"
      :key="child.master_id"
      :node="child"
      :depth="depth + 1"
      @delete="$emit('delete', $event)"
    />
  </div>
</template>

<script setup lang="ts">
import type { MasterCategory } from '@/stores/master'

defineProps<{
  node: MasterCategory
  depth: number
}>()

defineEmits<{
  (e: 'delete', masterId: string): void
}>()
</script>

<style scoped>
.master-node {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem 0;
  font-size: 0.9rem;
  color: #2c3e50;
}

.node-icon { color: #bdc3c7; font-size: 0.8rem; }

.node-name { flex: 1; }

.delete-btn {
  background: none;
  border: none;
  color: #bdc3c7;
  cursor: pointer;
  font-size: 0.8rem;
  padding: 0.1rem 0.3rem;
  border-radius: 3px;
  transition: color 0.2s;
}

.delete-btn:hover { color: #e74c3c; }
</style>
