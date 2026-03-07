<template>
  <div class="category-node" :style="{ marginLeft: depth * 20 + 'px' }">
    <div class="node-row">
      <input
        v-model="node.name"
        type="text"
        :placeholder="`カテゴリ名を入力（階層 ${depth + 1}）`"
        class="node-input"
      />
      <button type="button" class="btn-add" @click="$emit('add-child', node.id)">＋</button>
      <button type="button" class="btn-remove" @click="$emit('remove-node', node.id)">×</button>
    </div>

    <!-- 子カテゴリを再帰的に表示 -->
    <CategoryNode
      v-for="child in node.children"
      :key="child.id"
      :node="child"
      :depth="depth + 1"
      @add-child="$emit('add-child', $event)"
      @remove-node="$emit('remove-node', $event)"
    />
  </div>
</template>

<script setup lang="ts">
interface CategoryNodeType {
  id: string
  name: string
  children: CategoryNodeType[]
}

defineProps<{
  node: CategoryNodeType
  depth: number
}>()

defineEmits<{
  (e: 'add-child', id: string): void
  (e: 'remove-node', id: string): void
}>()
</script>

<style scoped>
.category-node {
  margin-bottom: 0.5rem;
}

.node-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.4rem;
}

.node-input {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border: 1px solid #dce1e7;
  border-radius: 6px;
  font-size: 0.9rem;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.node-input:focus {
  outline: none;
  border-color: #3498db;
}

.btn-add {
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  width: 2rem;
  height: 2rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-add:hover {
  background-color: #2980b9;
}

.btn-remove {
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 6px;
  width: 2rem;
  height: 2rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-remove:hover {
  background-color: #c0392b;
}
</style>
