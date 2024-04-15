<script setup lang="ts">
import { ref } from 'vue';

const light = ref<boolean>(!window.matchMedia('(prefers-color-scheme: dark)'));
</script>

<template>
    <div :class="[(light ? '!bg-gray-100' : ''), 'flex w-full flex-col justify-center items-center mt-3rem pt-2rem']"
        style="background-color: var(--p-menubar-background);">
        <div class="w-full flex flex-row justify-end px-3">
            <Button icon="pi pi-discord" plain text></Button>
            <Button icon="pi pi-youtube" plain text></Button>
            <Button icon="pi pi-github" plain text></Button>
        </div>
        <Divider></Divider>
        <div class="flex justify-center pb-3rem pt-2rem">
            <span class="text-sm">Copyright 2011-PRESENT © Noctisynth, org.</span>
        </div>
    </div>
</template>

<style scoped></style>