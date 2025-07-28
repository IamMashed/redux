<template>
	<v-dialog
		v-model="show"
		content-class="elevation-0"
		max-width="1000">

		<v-toolbar
			dark
			dense
			color="transparent"
			class="elevation-0">
			<v-spacer></v-spacer>
			<v-btn
				icon
				dark
				@click="show = false">
				<v-icon>mdi-close</v-icon>
			</v-btn>
        </v-toolbar>

		<swiper
			:options="swiperGalleryOption"
			class="swiper swiper-gallery"
			ref="swiperGallery"
			@ready="linkSwipers">
			<swiper-slide
				v-for="(photo, key) in photos"
				:key="key"
				:style="`background-image:url('${photo.url}');`"
				class="d-flex justify-center align-end">
				<div class="d-flex align-center mb-2">
				<v-checkbox
					v-model="photos[key].is_best"
					label="IS BEST"
					hide-details
					dark
					class="mt-0 mr-10"
					@change="updatePhoto(photo)">
				</v-checkbox>
				<v-btn
					color="error"
					elevation="0"
					fab
					small
					class="mr-10"
					@click="deletePhoto(photo.id)">
					<v-icon center>mdi-delete</v-icon>
				</v-btn>
				<v-btn
					color="white"
					elevation="0"
					fab
					small
					@click="slideToLastSlide">
					<v-icon center>mdi-plus</v-icon>
				</v-btn>
				</div>
			</swiper-slide>
			<swiper-slide class="d-flex justify-center align-center">
				<v-col cols="6">
					<v-card>
						<v-card-title>
							Add photo
						</v-card-title>
						<v-container>
							<v-col cols="11">
								<photo-upload
									ref="photoUpload"
									@upload="uploadPhoto">
								</photo-upload>
							</v-col>
						</v-container>
					</v-card>
				</v-col>
			</swiper-slide>

			<div class="swiper-button-next swiper-button-white" slot="button-next"></div>
			<div class="swiper-button-prev swiper-button-white" slot="button-prev"></div>
		</swiper>

		<swiper
			:options="swiperThumbsOption"
			class="swiper gallery-thumbs"
			ref="swiperThumbs">
			<swiper-slide
				v-for="(photo, key) in photos"
				:key="key"
				:style="`background-image:url('${photo.url}');`">
			</swiper-slide>
			<swiper-slide class="d-flex justify-center align-center white-transparent">
				<v-btn
					dark
					color="transparent"
					elevation="0"
					fab
					small>
					<v-icon center>mdi-plus</v-icon>
				</v-btn>
			</swiper-slide>

			<div class="swiper-button-next swiper-button-white swiper-button-small" slot="button-next"></div>
			<div class="swiper-button-prev swiper-button-white swiper-button-small" slot="button-prev"></div>
		</swiper>

		<confirm ref="confirm"></confirm>

	</v-dialog>
</template>

<script>
import { Swiper, SwiperSlide } from 'vue-awesome-swiper'
import PhotoUpload from './PhotoUpload'
import Confirm from './Confirm'

import 'swiper/css/swiper.css'

export default {
	components: {
		Swiper,
		SwiperSlide,
		PhotoUpload,
		Confirm,
	},
	props: {
		photos: {
			type: Array,
			default: () => ([]),
		},
	},
	data: () => ({
		show: false,
		swiperGalleryOption: {
			spaceBetween: 10,
			navigation: {
				nextEl: '.swiper-button-next',
				prevEl: '.swiper-button-prev',
			},
			observer: true,
			observeParents: true,
        },
        swiperThumbsOption: {
			spaceBetween: 10,
			navigation: {
				nextEl: '.swiper-button-next',
				prevEl: '.swiper-button-prev',
			},
			centeredSlides: true,
			slidesPerView: 'auto',
			touchRatio: 0.2,
			slideToClickedSlide: true,
			observer: true,
			observeParents: true,
        },
	}),
	methods: {
		open() {
			this.show = true
		},
		linkSwipers() {
			this.$nextTick(() => {
				const swiperGallery = this.$refs.swiperGallery.$swiper
				const swiperThumbs = this.$refs.swiperThumbs.$swiper
				swiperGallery.controller.control = swiperThumbs
				swiperThumbs.controller.control = swiperGallery
			})
		},

		uploadPhoto(file = File) {
			this.$emit('upload-photo', file)
			this.$refs.photoUpload.file = null
		},

		updatePhoto(photo) {
			this.$emit('update-photo', photo)
		},

		async deletePhoto(id) {
			const confirm = await this.$refs.confirm.open('Delete photo', 'Are you sure you want to delete photo?', { color: 'error' })
			if(confirm) this.$emit('delete-photo', id)
		},

		slideToLastSlide() {
			const swiperThumbs = this.$refs.swiperThumbs.$swiper
			swiperThumbs.slideTo(this.photos.length)
		},
	},
}
</script>

<style lang="scss" scoped>

.swiper {
	.swiper-slide {
		background-size: contain;
		background-position: center;

		&.white-transparent {
			background-color: rgba(255, 255, 255, 0.5);
		}
	}

	.swiper-button-small.swiper-button-prev::after,
	.swiper-button-small.swiper-button-next::after {
		font-size: 20px;
	}

	&.swiper-gallery {
		height: 65vh;
		width: 100%;
	}
	&.gallery-thumbs {
		height: 15vh;
		box-sizing: border-box;
		padding: 10px 0;
	}
	&.gallery-thumbs .swiper-slide {
		width: 12.5%;
		height: 100%;
		cursor: pointer;
		border: 3px solid transparent;
		background-size: cover;
	}
	&.gallery-thumbs .swiper-slide-active {
		opacity: 1;
		border-color: var(--v-primary-base);
	}
}

</style>