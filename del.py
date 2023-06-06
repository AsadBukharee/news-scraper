prohibited = ['.svg','/svg','ad.vidverto','outbrainimg','youtube','facebok','instagram','meta']
image_source = ['https://ad.vidverto.io/vidverto/player/logo.svg','https://mediaaws.almasryalyoum.com/news/small/2023/05/17/2106564_0.jpg', 'data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22640%22%20height%3D%22360%22%3E%3C%2Fsvg%3E', 'data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22640%22%20height%3D%22360%22%3E%3C%2Fsvg%3E', 'data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22640%22%20height%3D%22360%22%3E%3C%2Fsvg%3E', 'data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22640%22%20height%3D%22360%22%3E%3C%2Fsvg%3E', 'data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22640%22%20height%3D%22360%22%3E%3C%2Fsvg%3E', 'data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22640%22%20height%3D%22360%22%3E%3C%2Fsvg%3E', 'https://ad.vidverto.io/vidverto/player/logo.svg', 'https://ad.vidverto.io/vidverto/player/logo.svg', 'https://ad.vidverto.io/vidverto/player/logo.svg', 'https://ad.vidverto.io/vidverto/player/logo.svg', 'https://ad.vidverto.io/vidverto/player/logo.svg', 'https://ad.vidverto.io/vidverto/player/logo.svg', 'https://ad.vidverto.io/vidverto/player/logo.svg', 'https://ad.vidverto.io/vidverto/player/logo.svg', 'https://ad.vidverto.io/vidverto/player/logo.svg', 'https://ad.vidverto.io/vidverto/player/logo.svg', 'https://ad.vidverto.io/vidverto/player/logo.svg', 'https://ad.vidverto.io/vidverto/player/logo.svg', 'https://ad.vidverto.io/vidverto/player/logo.svg', 'https://ad.vidverto.io/vidverto/player/logo.svg']
for source in image_source:
    if not any(substr in source for substr in prohibited):
        print(source)