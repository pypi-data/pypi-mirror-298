<svelte:options accessors={true} />

<script lang="ts">
	import { onMount } from "svelte";
	import type { Gradio } from "@gradio/utils";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import { tick } from "svelte";

	export let gradio: Gradio<{
		change: never;
		submit: never;
		input: never;
		clear_status: LoadingStatus;
	}>;
	export let label = "Textbox";
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value = "";
	export let placeholder = "";
	export let show_label: boolean;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus | undefined = undefined;
	export let value_is_output = false;
	export let interactive: boolean;
	export let rtl = false;
	export let width: number;
	export let height: number;
	export let accept: string | null;
	export let appKey: string;
	export let appAccessKey: string | undefined;
	export let clientName: string | undefined;

	let el: HTMLTextAreaElement | HTMLInputElement;
	const container = true;

	let accessKey;
	let xAppKey;
	function setCookieMap() {
		let cookieMap = new Map();
		document.cookie.split(";").forEach((cookie) => {
			const [key, value] = cookie.trim().split("=");
			cookieMap.set(key, value);
		});
		accessKey = appAccessKey ?? cookieMap.get('appAccessKey')
		xAppKey = clientName ?? cookieMap.get('clientName')
	}
	function handle_change(): void {
		gradio.dispatch("change");
		if (!value_is_output) {
			gradio.dispatch("input");
		}
	}

	async function submit(): Promise<void> {
		await tick();
		gradio.dispatch("submit");
	}

	$: if (value === null) value = "";

	// When the value changes, dispatch the change event via handle_change()
	// See the docs for an explanation: https://svelte.dev/docs/svelte-components#script-3-$-marks-a-statement-as-reactive
	$: value, handle_change();

	let iframeRef;

	const init = () => {
		const deploymentId = window.location.search.match(/deploymentId=([^&]*)/)?.[1] ?? '';
		const scene = window.location.search.match(/mode=([^&]*)/)?.[1] ?? '';
		if (appKey && iframeRef?.contentWindow) {
			iframeRef.contentWindow.postMessage({
				id: '1',
				type: 'selectFromBohrium',
				data: {
					accept,
					appKey,
					deploymentId: deploymentId ? +deploymentId : undefined,
					scene: scene ? scene : undefined,
					directory: false,
				},
				headers: {
					accessKey,
					'x-app-key': xAppKey,
				}
			}, '*')
		}
	}
	$: accept, init();
	$: appKey, init();
	$: visible, init();

	onMount(() => {
		setCookieMap();
		iframeRef.onload = () => {
			init();
		}
		window.addEventListener("message", async function(e: any) {
			const { data: res } = e 
			if (res.type === 'selectFromBohrium' && res.status === 'succeed') {
				value = encodeURI(decodeURIComponent(res.data.url));
				iframeRef.contentWindow.postMessage({
					id: '1',
					type: 'clear',
					data: {},
					headers: {
						accessKey,
						'x-app-key': xAppKey,
					}
				}, '*')	
			}
			if (res.type === 'closeWindow') {
				submit();
				iframeRef.contentWindow.postMessage({
					id: '1',
					type: 'clear',
					data: {},
					headers: {
						accessKey,
						'x-app-key': xAppKey,
					}
				}, '*')	
			}
			if (res.type === 'ready') {
				init();
			}
		})
	});
</script>

<Block
	{visible}
	{elem_id}
	{elem_classes}
	{scale}
	{min_width}
	allow_overflow={false}
	padding={true}
>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
			on:clear_status={() =>
				gradio.dispatch("clear_status", loading_status)}
		/>
	{/if}
	<iframe src="https://bohrium.dp.tech/app/function-panel" bind:this={iframeRef} style="width:{width}px;height: {height}px;padding: 24px;background: #ffffff;{visible ? '' : 'display: none;'}"></iframe>
</Block>

<style>
	label {
		display: block;
		width: 100%;
	}

	input {
		display: block;
		position: relative;
		outline: none !important;
		box-shadow: var(--input-shadow);
		background: var(--input-background-fill);
		padding: var(--input-padding);
		width: 100%;
		color: var(--body-text-color);
		font-weight: var(--input-text-weight);
		font-size: var(--input-text-size);
		line-height: var(--line-sm);
		border: none;
	}
	.container > input {
		border: var(--input-border-width) solid var(--input-border-color);
		border-radius: var(--input-radius);
	}
	input:disabled {
		-webkit-text-fill-color: var(--body-text-color);
		-webkit-opacity: 1;
		opacity: 1;
	}

	input:focus {
		box-shadow: var(--input-shadow-focus);
		border-color: var(--input-border-color-focus);
	}

	input::placeholder {
		color: var(--input-placeholder-color);
	}
</style>
