# Per-guide page metadata. The label is the audience marker shown on the index
# and as the page eyebrow; "For developers" is the one that warns a general
# reader off, which was the point of labelling them at all.
META = {
 "ai-image-generation-offline-iphone": dict(
   label="Start here",
   blurb="What on-device generation actually means, what it costs you, and how to verify the offline claim yourself.",
   desc="Yes, once the model is downloaded. What on-device AI image generation means on an iPhone, what it costs in storage and setup time, and how to test the offline claim yourself in airplane mode."),
 "will-my-iphone-run-on-device-ai-images": dict(
   label="Before you buy",
   blurb="It is decided by memory, not age. The numbers, the device list, and what to do if yours does not qualify.",
   desc="Whether an iPhone or iPad can run an on-device AI image generator is decided by memory, not age. The 6 GB and 12 GB requirements, which devices clear them, storage to budget, and the options if yours does not."),
 "write-better-ai-image-prompts": dict(
   label="Getting better results",
   blurb="Why longer prompts get worse, where the hard limit sits, and a structure that works in fourteen words.",
   desc="Why longer AI image prompts get worse results, where the hard limit sits, and a four-part structure that works in about fourteen words. Written for on-device models, useful for any of them."),
 "stable-diffusion-on-iphone-explained": dict(
   label="For developers",
   blurb="Conversion, quantization, splitting the model, and why the Neural Engine beats the GPU for this.",
   desc="How Stable Diffusion is made to run on an iPhone or iPad: Core ML conversion, 6-bit palettization, splitting the UNet into chunks, step-distilled sampling, and why the Neural Engine beats the GPU here."),
 "upscale-photo-4k-iphone": dict(
   label="How to",
   blurb="The difference between resizing and upscaling, what it can rebuild, and what it cannot.",
   desc="How to upscale a photo to 4K on an iPhone without uploading it. The difference between resizing and upscaling, what an upscaling model can rebuild, what it cannot, and how to choose an output size."),
 "make-ai-wallpaper-iphone": dict(
   label="How to",
   blurb="Composing for the clock and the dock, prompts that reliably work, and why you crop rather than stretch.",
   desc="How to make a custom AI wallpaper for an iPhone: composing around the clock and the dock, prompt styles that reliably work at phone proportions, and why you crop to shape rather than stretch."),
 "ai-image-generator-no-subscription": dict(
   label="Before you buy",
   blurb="Why on-device generation makes one-time pricing possible, and what to check before paying.",
   desc="Why almost every AI image generator is a subscription, how running on the device makes one-time pricing possible, and the specific things to check before you pay for one."),
 "anime-art-from-text-iphone": dict(
   label="How to",
   blurb="What a general model can and cannot do with anime, and how to prompt for it.",
   desc="How to create anime and illustrated art from text on an iPhone or iPad. What a general-purpose model does well in that style, where it falls short of a dedicated one, and how to prompt for it."),
 "on-device-vs-cloud-ai-image-generators": dict(
   label="Before you buy",
   blurb="An honest comparison, including the cases where cloud is simply better.",
   desc="On-device or cloud AI image generation: an honest comparison of image quality, cost, privacy, speed and limits, including the cases where a cloud generator is simply the better choice."),
 "vs-apple-image-playground": dict(
   label="Before you buy",
   blurb="Two different propositions. Which one fits what you actually want to make.",
   desc="Apple's Image Playground and third-party on-device generators answer different questions. What each one is for, what each will and will not draw, and which fits what you want to make."),
}

# Index order, which is not the order they were drafted in: the two questions a
# stranger actually arrives with come first, then the ones that need a decision.
ORDER = ["ai-image-generation-offline-iphone", "will-my-iphone-run-on-device-ai-images",
         "write-better-ai-image-prompts", "upscale-photo-4k-iphone",
         "make-ai-wallpaper-iphone", "anime-art-from-text-iphone",
         "ai-image-generator-no-subscription", "on-device-vs-cloud-ai-image-generators",
         "vs-apple-image-playground", "stable-diffusion-on-iphone-explained"]
