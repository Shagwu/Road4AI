# Blotato Media Strategy

## Purpose

Every LinkedIn post gets a visual. Variety across posts. Zero text-only LinkedIn content going forward.

## Visual Types

| Type | Template ID | Use When | Credits (est.) |
|------|-------------|----------|----------------|
| Carousel (5-6 slides) | `53cfec04-2500-41cf-8cc1-ba670d2c341a` | Long-form storytelling, multi-step lessons | ~300-500 |
| Quote Card | `f941e306-76f7-45da-b3d9-7463af630e91` | Single punchy insight, opinion piece | ~100-200 |
| Single Image | `9f4e66cd-b784-4c02-b2ce-e6d0765fd4c0` | Clean, minimal, text-forward | ~100-200 |
| Tutorial Carousel | `e095104b-e6c5-4a81-a89d-b0df3d7c5baf` | Step-by-step how-to content | ~300-500 |
| AI Story Video | `5903fe43-514d-40ee-a060-0d6628c5f8fd` | Narrative with visual motion | ~500-1000 |

## Variety Rule

No two consecutive LinkedIn posts use the same visual type.

Default cycle: Carousel → Quote Card → Image → Tutorial → Video → repeat.

When in doubt, pick the type that best serves the post's structure:
- Multi-step arc → Carousel
- Single insight → Quote Card
- Clean close → Single Image
- How-to → Tutorial Carousel
- Story with emotion → AI Story Video

## Visual Style

Brand: black and emerald terminal aesthetic.

- Dark backgrounds (black or near-black)
- Emerald green (#00D26A or similar) for accents, dividers, highlights
- Bold white sans-serif text for headlines
- Smaller emerald text for labels, slide numbers
- No corporate stock photos. No gradient backgrounds. No emojis in visuals.
- Terminal/coding aesthetic where possible (monospace fonts, cursor blinks, command-line motifs)

## How It Works

### 1. Draft Gets Visual Metadata

Each LinkedIn draft includes in frontmatter:
```yaml
visual_type: carousel  # carousel | quote_card | image | tutorial | video
```

And in the body, one or more `**Blotato image prompt:**` blocks:
```markdown
**Blotato image prompt:**
Dark slide with emerald accent bar. Bold white text: "The hook goes here." Small emerald label: "1/5". Black background, terminal aesthetic.
```

### 2. schedule_post.py Reads Visual Type

The `generate_visual` function in `schedule_post.py`:
1. Reads `visual_type` from frontmatter
2. Looks up template ID from `VISUAL_TEMPLATES` dict
3. Extracts `**Blotato image prompt:**` blocks from the draft
4. Calls `blotato_create_visual` with template ID and prompt
5. Polls `blotato_get_visual_status` for completion
6. Passes resulting `imageUrls` (or `mediaUrl` for video) to `blotato_create_post`

### 3. X Posts Stay Text-Only

X/Twitter posts do not get visuals. The 280-char constraint and thread format don't benefit from carousel/video media. LinkedIn is the visual platform.

## Credit Budget

- 20K free credits available
- ~3 LinkedIn posts/week with visuals
- Average ~300 credits per visual
- Monthly cost: ~3,600 credits
- Runway: ~5.5 months at current pace

## Template Notes

- Carousel templates accept a `prompt` that describes the slides. Blotato's AI generates the slide content from the prompt.
- Quote card templates accept a prompt with the key quote. AI styles it.
- Single image template is the existing `9f4e66cd` — already proven in production.
- Video templates may take 30-60 seconds to generate. Poll timeout increased to 300s.
- If a template fails, fall back to single image (always works).

## Troubleshooting

- If visual generation fails, check `my.blotato.com/videos/<ID>` to view and manually edit
- If template not found, run `blotato_list_visual_templates` to refresh the catalog
- If credits run low, prioritize quote cards and single images (cheapest)
