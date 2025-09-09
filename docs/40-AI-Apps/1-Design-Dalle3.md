---
title: "Design with DALL-E"
slug: /40-AI-Apps-Design
---

:::info TUTORIAL OVERVIEW
In this tutorial, you'll learn how to leverage AI for product design by integrating DALL-E image generation into a web application.

**What you'll build:** A design generation feature that creates visual concepts from text descriptions.

**What you'll learn:**
- How to integrate DALL-E with Azure OpenAI
- Image generation API implementation
- Error handling for content safety
- UI integration for AI-generated content
:::

## Learning Objectives

By the end of this tutorial, you will be able to:

1. **Understand DALL-E 3 Capabilities**: Learn about the latest features and improvements in OpenAI's image generation model
2. **Implement Azure OpenAI Integration**: Set up and configure Azure OpenAI for image generation with proper authentication and error handling
3. **Design Effective Prompts**: Create prompts that generate high-quality, relevant images for business use cases
4. **Handle Content Safety**: Implement content filtering and safety measures for generated images
5. **Build Production UI**: Create user-friendly interfaces for image generation with loading states and error handling
6. **Optimize for Business Use**: Apply image generation to real marketing and design workflows

## DALL-E 3 Deep Dive

### What Makes DALL-E 3 Special

DALL-E 3 represents a significant advancement in AI image generation:

**Enhanced Understanding**: 
- Improved comprehension of complex prompts with multiple objects and relationships
- Better handling of spatial relationships and positioning
- More accurate interpretation of artistic styles and techniques

**Higher Quality Output**:
- 1024x1024 pixel resolution for crisp, professional images
- Better consistency in generating human faces and hands
- Improved coherence in complex scenes with multiple elements

**Safety and Compliance**:
- Built-in content policy enforcement
- Automatic filtering of potentially harmful content
- Respect for artist styles and copyrighted material

**Business Applications**:
- Marketing material creation (social media posts, advertisements)
- Product mockups and prototyping
- Educational content and illustrations
- Creative brainstorming and ideation

![DALL-E 3 Capabilities Overview](images/dalle3-capabilities.png)

## Scenario

You're tasked with developing a feature that helps product designers generate creative concepts quickly. The goal is to develop visually compelling designs that align with brand values and enhance brand identity, ensuring they captivate customer interest and drive engagement.

## Challenge

Elevate product design creativity by harnessing the power of DALL-E model to generate unique, high-quality artwork. This will facilitate concept development, streamline the brainstorming process, and inspire innovative design solutions that push creative boundaries.

![Design Challenge](images/challenge-1.png)

## Step-by-Step Implementation

### Step 1: Understanding Azure OpenAI DALL-E Integration

Before implementing, understand the key components:

**Azure OpenAI Service Setup**:
- DALL-E 3 model deployment in your Azure OpenAI resource
- Proper endpoint configuration (e.g., `https://your-resource.openai.azure.com/`)
- API keys with appropriate permissions
- Region considerations for best performance

**API Structure**:
```typescript
// Azure OpenAI DALL-E endpoint pattern
const endpoint = "https://<resource-name>.openai.azure.com/";
const deploymentName = "dalle3"; // Your DALL-E deployment name
const apiVersion = "2024-02-01"; // Latest API version for DALL-E
```

![Azure OpenAI DALL-E Setup](images/azure-openai-dalle-setup.png)

### Step 2: Set Up Your Development Environment

**Prerequisites Check**:
```bash
# Verify Node.js and npm versions
node --version  # Should be 16+
npm --version

# Navigate to the chatbot application
cd apps-chat/chatbot

# Install dependencies if not already done
npm install

# Start development server
npm run dev
```

**Required Dependencies**:
```json
{
  "@azure/openai": "^1.0.0-beta.12",
  "react": "^18.0.0",
  "react-promise-tracker": "^2.1.0"
}
```

### Step 3: Examine the Existing Code Structure

Navigate to `apps-chat\chatbot\pages\design\Design.tsx` and review:

**Current Components**:
- Input field for prompt text
- Generate button to trigger DALL-E
- Image display area for results
- Loading state management

**Key Functions to Implement**:
- `dalleApi()`: Main function for DALL-E integration
- Error handling for content safety
- Image URL processing and display

### Step 4: Implement Professional DALL-E Integration

Here's the comprehensive implementation structure:

```typescript
import { OpenAIClient, AzureKeyCredential } from "@azure/openai";

async function dalleApi(prompt: string): Promise<string> {
    try {
        // Step 1: Configure Azure OpenAI client
        const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "https://your-resource.openai.azure.com/";
        const apiKey = process.env.AZURE_OPENAI_API_KEY || "your-api-key";
        
        const client = new OpenAIClient(
            endpoint,
            new AzureKeyCredential(apiKey)
        );

        // Step 2: Prepare image generation parameters
        const imageGenerationOptions = {
            prompt: prompt,
            size: "1024x1024" as const,
            n: 1,
            quality: "standard" as const,
            style: "vivid" as const
        };

        // Step 3: Call DALL-E API
        const deploymentName = "dalle3"; // Your deployment name
        const response = await client.getImages(
            deploymentName, 
            prompt, 
            imageGenerationOptions
        );

        // Step 4: Extract image URL
        if (response.data && response.data.length > 0) {
            const imageUrl = response.data[0].url;
            if (imageUrl) {
                return imageUrl;
            }
        }

        throw new Error("No image URL returned from DALL-E");

    } catch (error) {
        // Step 5: Handle specific error types
        if (error.status === 400) {
            throw new Error("Content policy violation: Please modify your prompt and try again");
        } else if (error.status === 429) {
            throw new Error("Rate limit exceeded: Please wait a moment before trying again");
        } else if (error.status === 500) {
            throw new Error("Service temporarily unavailable: Please try again later");
        } else {
            throw new Error(`Image generation failed: ${error.message}`);
        }
    }
}
```

### Step 5: Enhanced Prompt Engineering

**Effective Prompt Patterns**:

```typescript
// Product design prompts
const productPrompts = {
    logo: "Create a modern, minimalist logo for [company/product] with [color scheme], vector style, clean lines",
    packaging: "Design product packaging for [product] in [style], showing [features], professional photography style",
    marketing: "Create a marketing banner for [product/service] with [mood/tone], [target audience] focus, high quality",
    mockup: "Product mockup of [item] in [environment/setting], realistic lighting, commercial photography style"
};

// Style modifiers for different use cases
const styleModifiers = {
    professional: "clean, corporate, professional photography, high quality, studio lighting",
    creative: "artistic, creative, vibrant colors, dynamic composition, innovative design",
    minimalist: "minimalist, clean lines, simple, white background, modern design",
    vintage: "vintage style, retro colors, classic design elements, nostalgic feel"
};

// Example of building comprehensive prompts
function buildDesignPrompt(basePrompt: string, style: string, additionalDetails?: string): string {
    return `${basePrompt}, ${styleModifiers[style]}${additionalDetails ? `, ${additionalDetails}` : ''}, 4K resolution, professional quality`;
}
```

### Step 6: Advanced Error Handling and User Experience

```typescript
interface ImageGenerationState {
    isLoading: boolean;
    imageUrl: string | null;
    error: string | null;
    progress: number;
}

class ImageGenerationManager {
    private state: ImageGenerationState = {
        isLoading: false,
        imageUrl: null,
        error: null,
        progress: 0
    };

    async generateImage(prompt: string, onStateChange: (state: ImageGenerationState) => void): Promise<void> {
        // Update loading state
        this.updateState({ isLoading: true, error: null, progress: 25 }, onStateChange);

        try {
            // Validate prompt
            if (!this.validatePrompt(prompt)) {
                throw new Error("Please provide a more descriptive prompt (minimum 10 characters)");
            }

            this.updateState({ progress: 50 }, onStateChange);

            // Generate image
            const imageUrl = await dalleApi(prompt);
            
            this.updateState({ progress: 75 }, onStateChange);

            // Verify image accessibility
            await this.verifyImageUrl(imageUrl);
            
            this.updateState({ 
                isLoading: false, 
                imageUrl, 
                progress: 100 
            }, onStateChange);

        } catch (error) {
            this.updateState({ 
                isLoading: false, 
                error: error.message,
                progress: 0 
            }, onStateChange);
        }
    }

    private validatePrompt(prompt: string): boolean {
        return prompt.trim().length >= 10 && prompt.trim().length <= 1000;
    }

    private async verifyImageUrl(url: string): Promise<void> {
        // Test if image URL is accessible
        const response = await fetch(url, { method: 'HEAD' });
        if (!response.ok) {
            throw new Error("Generated image is not accessible");
        }
    }

    private updateState(updates: Partial<ImageGenerationState>, onStateChange: (state: ImageGenerationState) => void): void {
        this.state = { ...this.state, ...updates };
        onStateChange(this.state);
    }
}
```

## Advanced Considerations

Once you have the basic functionality working, consider these enhancements:

### Security
- Secure API key storage (environment variables, Azure Key Vault)
- Input validation and sanitization
- Rate limiting implementation

### Content Safety
- Handle content safety filter responses
- Provide user feedback for rejected content
- Implement fallback mechanisms

### User Experience
- Loading states and progress indicators
- Image download and save functionality
- Prompt suggestion features
- History of generated images

### Integration
- Integrate with the main chatbot conversation flow
- Save generated images to storage
- Share functionality

## Real-World Business Applications

### Marketing Campaign Creation
Build a comprehensive marketing asset generator:

```typescript
interface MarketingAssetGenerator {
    // Generate social media posts
    async generateSocialPost(product: string, platform: 'instagram' | 'facebook' | 'twitter'): Promise<string> {
        const platformSpecs = {
            instagram: "square 1024x1024, vibrant colors, lifestyle photography style",
            facebook: "landscape 1200x630, professional, engaging composition",
            twitter: "landscape 1024x512, clear messaging, eye-catching design"
        };
        
        const prompt = `Create a ${platformSpecs[platform]} social media post featuring ${product}, modern design, high quality, marketing photography`;
        return await dalleApi(prompt);
    }

    // Generate product mockups
    async generateProductMockup(product: string, context: string): Promise<string> {
        const prompt = `Product mockup of ${product} in ${context}, professional photography, realistic lighting, commercial quality, clean background`;
        return await dalleApi(prompt);
    }

    // Generate brand-consistent artwork
    async generateBrandArtwork(brandGuidelines: BrandGuidelines, concept: string): Promise<string> {
        const prompt = `${concept} in brand style: ${brandGuidelines.colorScheme}, ${brandGuidelines.style}, logo placement area, brand consistent, professional quality`;
        return await dalleApi(prompt);
    }
}

interface BrandGuidelines {
    colorScheme: string;
    style: string;
    logoPlacement: string;
    restrictions: string[];
}
```

### E-commerce Integration
Create product images for online stores:

```typescript
class EcommerceImageGenerator {
    async generateProductVariations(baseProduct: string, variations: string[]): Promise<string[]> {
        const images: string[] = [];
        
        for (const variation of variations) {
            const prompt = `${baseProduct} in ${variation}, product photography, white background, professional lighting, e-commerce style, high resolution`;
            try {
                const imageUrl = await dalleApi(prompt);
                images.push(imageUrl);
            } catch (error) {
                console.error(`Failed to generate ${variation}:`, error);
            }
        }
        
        return images;
    }

    async generateLifestyleShots(product: string, lifestyleContext: string): Promise<string> {
        const prompt = `${product} being used in ${lifestyleContext}, lifestyle photography, natural lighting, authentic setting, people interacting with product`;
        return await dalleApi(prompt);
    }
}
```

### Content Creation Workflow
Automated content pipeline for different media:

```typescript
class ContentCreationPipeline {
    async createContentSeries(theme: string, formats: ContentFormat[]): Promise<ContentAsset[]> {
        const assets: ContentAsset[] = [];
        
        for (const format of formats) {
            try {
                const prompt = this.buildFormatSpecificPrompt(theme, format);
                const imageUrl = await dalleApi(prompt);
                
                assets.push({
                    format,
                    imageUrl,
                    prompt,
                    generatedAt: new Date(),
                    status: 'ready'
                });
            } catch (error) {
                assets.push({
                    format,
                    imageUrl: null,
                    prompt: '',
                    generatedAt: new Date(),
                    status: 'failed',
                    error: error.message
                });
            }
        }
        
        return assets;
    }

    private buildFormatSpecificPrompt(theme: string, format: ContentFormat): string {
        const formatSpecs = {
            'blog-header': '1200x400 banner style, text overlay area, professional',
            'social-square': '1024x1024 square format, engaging, social media optimized',
            'email-banner': '600x200 email header, clear messaging area, professional',
            'presentation-slide': '1920x1080 presentation background, clean, minimal text area'
        };
        
        return `${theme}, ${formatSpecs[format.type]}, high quality, professional design`;
    }
}

interface ContentFormat {
    type: 'blog-header' | 'social-square' | 'email-banner' | 'presentation-slide';
    dimensions: string;
    requirements: string[];
}

interface ContentAsset {
    format: ContentFormat;
    imageUrl: string | null;
    prompt: string;
    generatedAt: Date;
    status: 'ready' | 'failed' | 'processing';
    error?: string;
}
```

## Performance Optimization and Scaling

### Caching Strategy
Implement intelligent caching to reduce costs and improve performance:

```typescript
class ImageGenerationCache {
    private cache = new Map<string, CacheEntry>();
    private readonly CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours

    async getOrGenerate(prompt: string): Promise<string> {
        // Check cache first
        const cached = this.getCached(prompt);
        if (cached) {
            return cached.imageUrl;
        }

        // Generate new image
        const imageUrl = await dalleApi(prompt);
        
        // Cache the result
        this.setCached(prompt, imageUrl);
        
        return imageUrl;
    }

    private getCached(prompt: string): CacheEntry | null {
        const entry = this.cache.get(this.hashPrompt(prompt));
        if (entry && (Date.now() - entry.timestamp) < this.CACHE_DURATION) {
            return entry;
        }
        return null;
    }

    private setCached(prompt: string, imageUrl: string): void {
        this.cache.set(this.hashPrompt(prompt), {
            imageUrl,
            timestamp: Date.now(),
            prompt
        });
    }

    private hashPrompt(prompt: string): string {
        // Simple hash function for demonstration
        return btoa(prompt).replace(/[^a-zA-Z0-9]/g, '').substring(0, 32);
    }
}

interface CacheEntry {
    imageUrl: string;
    timestamp: number;
    prompt: string;
}
```

### Batch Processing
Handle multiple image generation requests efficiently:

```typescript
class BatchImageGenerator {
    private queue: ImageRequest[] = [];
    private processing = false;
    private readonly BATCH_SIZE = 3;
    private readonly DELAY_BETWEEN_BATCHES = 2000; // 2 seconds

    async queueGeneration(request: ImageRequest): Promise<string> {
        return new Promise((resolve, reject) => {
            this.queue.push({
                ...request,
                resolve,
                reject
            });
            
            this.processBatch();
        });
    }

    private async processBatch(): Promise<void> {
        if (this.processing || this.queue.length === 0) return;
        
        this.processing = true;
        
        try {
            const batch = this.queue.splice(0, this.BATCH_SIZE);
            
            // Process batch concurrently with individual error handling
            const promises = batch.map(async (request) => {
                try {
                    const result = await dalleApi(request.prompt);
                    request.resolve(result);
                } catch (error) {
                    request.reject(error);
                }
            });
            
            await Promise.allSettled(promises);
            
            // Delay before processing next batch
            if (this.queue.length > 0) {
                setTimeout(() => {
                    this.processing = false;
                    this.processBatch();
                }, this.DELAY_BETWEEN_BATCHES);
            } else {
                this.processing = false;
            }
            
        } catch (error) {
            this.processing = false;
            console.error('Batch processing error:', error);
        }
    }
}

interface ImageRequest {
    prompt: string;
    resolve?: (result: string) => void;
    reject?: (error: Error) => void;
}
```

## Solution Reference

<details>
<summary>View Complete Solution</summary>
<details>
<summary>Try implementing it yourself first!</summary>
<details>
<summary>Click to reveal the solution code</summary>

```typescript
import React, { useState } from "react";
import { trackPromise } from "react-promise-tracker";
import { usePromiseTracker } from "react-promise-tracker";
import { OpenAIClient, AzureKeyCredential, Completions } from '@azure/openai';

const Page = () => {
    const { promiseInProgress } = usePromiseTracker();
    const [imageText, setImageText] = useState<string>();
    const [imageUrl, setImageUrl] = useState<string>("");

    async function process() {
        if (imageText != null) {
            trackPromise(
                dalleApi(imageText)
            ).then((res) => {
                setImageUrl(res);
            })
        }
    }

    async function dalleApi(prompt: string): Promise<string> {
        const options = {
            api_version: "2024-02-01"
        };
        const size = '1024x1024';
        const n = 1;
        
        var openai_url = "https://arg-syd-aiaaa-openai.openai.azure.com";
        var openai_key = "<API_KEY>";
        const client = new OpenAIClient(
            openai_url,
            new AzureKeyCredential(openai_key),
            options
        );

        const deploymentName = 'dalle3';
        const result = await client.getImages(deploymentName, prompt, { n, size });
        console.log(result);

        if (result.data[0].url) {
            return result.data[0].url;
        } else {
            throw new Error("Image URL is undefined");
        }
    }

    const updateText = (e: React.ChangeEvent<HTMLInputElement>) => {
        setImageText(e.target.value);
    };

    return (
        <div className="pageContainer">
            <h2>Design</h2>
            <p></p>
            <p>
                <input type="text" placeholder="(describe your design here)" onChange={updateText} />
                <button onClick={() => process()}>Generate</button><br />
                {
                    (promiseInProgress === true) ?
                        <span>Loading...</span>
                        :
                        null
                }
            </p>
            <p>
                <img height={"550px"} src={imageUrl} />
            </p>
        </div>
    );
};

export default Page;
```

</details>
</details>
</details>

## Next Steps

Once you've completed this tutorial, you can:
1. Move on to Tutorial 2: Translation Services
2. Explore integrating multiple AI services
3. Build more complex design workflows
4. Add user authentication and personalization

## Additional Resources

- [Azure OpenAI DALL-E Documentation](https://docs.microsoft.com/azure/cognitive-services/openai/dall-e-quickstart)
- [Content Safety Guidelines](https://docs.microsoft.com/azure/cognitive-services/content-safety/)
- [OpenAI Client SDK Documentation](https://docs.microsoft.com/javascript/api/@azure/openai/)
