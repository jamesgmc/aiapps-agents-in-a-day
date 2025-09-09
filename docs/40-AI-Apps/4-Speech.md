---
title: "Speech Processing"
slug: /40-AI-Apps-Speech
---

:::info TUTORIAL OVERVIEW
In this tutorial, you'll learn how to implement text-to-speech capabilities using Azure Speech Services to enhance accessibility and user experience.

**What you'll build:** A speech synthesis system that converts text to natural-sounding speech.

**What you'll learn:**
- Azure Speech Services integration
- Browser audio playback
- Accessibility considerations
- Speech synthesis customization
:::

## Learning Objectives

By the end of this tutorial, you will be able to:

1. **Master Azure Speech Services**: Understand the comprehensive capabilities of Azure's speech platform including neural voices, SSML, and custom voice models
2. **Implement Professional Speech Synthesis**: Build robust text-to-speech features with advanced voice customization and audio optimization
3. **Design Accessible Voice Interfaces**: Create inclusive experiences that serve users with visual impairments and different accessibility needs
4. **Handle Multi-language Speech**: Support global audiences with regional accents, pronunciation, and cultural considerations
5. **Optimize Audio Performance**: Implement efficient audio streaming, caching, and browser compatibility strategies
6. **Build Voice-Enabled Applications**: Create comprehensive voice interfaces for customer service, education, and accessibility

## Azure Speech Services Deep Dive

### Service Architecture

Azure Speech Services offers a comprehensive platform for speech processing:

**Text-to-Speech (TTS)**:
- 400+ neural voices across 140+ languages and locales
- Custom neural voice creation for brand consistency
- SSML support for precise pronunciation control
- Real-time streaming and batch processing capabilities

**Speech-to-Text (STT)**:
- Real-time transcription with high accuracy
- Custom speech models for domain-specific vocabulary
- Speaker identification and diarization
- Multi-channel audio processing

**Voice Assistants**:
- Custom keyword recognition
- Intent recognition integration
- Conversation flow management
- Multi-turn dialog support

![Azure Speech Services Overview](images/azure-speech-services.png)

### Neural Voice Technology

**Standard vs Neural Voices**:
- **Standard Voices**: Traditional concatenative synthesis
- **Neural Voices**: AI-powered, human-like speech quality
- **Custom Neural Voices**: Brand-specific voice training
- **Personal Voice**: Clone voices with minimal training data

**Voice Characteristics**:
- **Pitch and Tone Control**: Adjust emotional expression
- **Speaking Rate**: Customize delivery speed
- **Pronunciation**: Fine-tune specific words and phrases
- **Pausing and Emphasis**: Control rhythm and flow

**Regional Variations**:
- Accent-specific voices (US, UK, Australian English)
- Cultural pronunciation preferences
- Regional dialect support
- Local language nuances

## Scenario

Your retail store wants to enhance accessibility and provide a more natural, engaging experience for customers. The goal is to implement text-to-speech (TTS) to improve efficiency and self-service capabilities, allowing shoppers to receive audio information about products, navigation, and promotions.

## Challenge

Implement text-to-speech functionality that reduces reliance on staff while maintaining a personalized touch through natural-sounding voice interactions.

![Speech Challenge](images/challenge-4.png)

## Step-by-Step Implementation

### Step 1: Understanding Azure Speech Services

Azure Speech Services provides:
- High-quality neural voices
- Multiple languages and accents
- SSML (Speech Synthesis Markup Language) support
- Real-time and batch processing
- Customizable voice models

### Step 2: Examine the Speech Component

Navigate to `apps-chat\chatbot\pages\speech\Speech.tsx`. You'll find:
- A text input for content to be spoken
- A read button to trigger speech synthesis
- Placeholder for audio playback controls

### Step 3: Set Up Speech Configuration

Before implementing the speech API, you need to:
- Configure the Speech SDK
- Set up authentication with your Speech service
- Choose appropriate voice and language settings

```typescript
useEffect(() => {
    const speechConfig = SpeechConfig.fromSubscription(
        'YOUR_SPEECH_KEY', 
        'YOUR_REGION'
    );
    
    // Configure voice settings
    speechConfig.speechSynthesisVoiceName = 'en-US-AriaNeural';
    speechConfig.speechSynthesisOutputFormat = SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3;
    
    // Initialize synthesizer
    const synthesizer = new SpeechSynthesizer(speechConfig);
}, []);
```

### Step 4: Implement Speech Synthesis

Your task is to complete the `speechApi` function to:
- Convert text to speech using Azure Speech Services
- Handle the audio output appropriately
- Manage playback in the browser
- Provide user feedback during processing

#### Key Implementation Steps:
```typescript
async function speechApi(text: string): Promise<void> {
    return new Promise((resolve, reject) => {
        synthesizer.speakTextAsync(
            text,
            result => {
                // Handle successful synthesis
                // Play audio in browser
                resolve();
            },
            error => {
                // Handle errors
                reject(error);
            }
        );
    });
}
```

### Step 5: Advanced Speech Features

#### SSML for Enhanced Control
```typescript
const ssmlText = `
<speak version="1.0" xml:lang="en-US">
    <voice name="en-US-AriaNeural">
        <prosody rate="medium" pitch="medium">
            Welcome to our store! 
            <break time="500ms"/>
            How can I help you today?
        </prosody>
    </voice>
</speak>`;
```

#### Voice Customization Options
```typescript
const voiceOptions = {
    'en-US-AriaNeural': 'Professional female voice',
    'en-US-DavisNeural': 'Professional male voice',
    'en-US-JennyNeural': 'Friendly female voice',
    'en-US-GuyNeural': 'Casual male voice'
};
```

#### Audio Format Selection
```typescript
const audioFormats = {
    mp3: SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3,
    wav: SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm,
    ogg: SpeechSynthesisOutputFormat.OggOpusMonoMp3
};
```

### Step 6: Browser Audio Integration

Implement audio playback in the browser:

```typescript
function playAudioBuffer(audioData: ArrayBuffer) {
    const audioContext = new AudioContext();
    const audioBuffer = await audioContext.decodeAudioData(audioData);
    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContext.destination);
    source.start();
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
import React, { useState, useEffect, useRef } from "react";
import { trackPromise } from "react-promise-tracker";
import { usePromiseTracker } from "react-promise-tracker";
import * as sdk from 'microsoft-cognitiveservices-speech-sdk';

const Page = () => {
    const { promiseInProgress } = usePromiseTracker();
    const [speechText, setSpeechText] = useState<string>("");
    const synthesizerRef = useRef<sdk.SpeechSynthesizer | null>(null);
    const speechConfigRef = useRef<sdk.SpeechConfig | null>(null);

    useEffect(() => {
        const speech_key = '<API_KEY>';
        const speech_region = 'eastus';
        
        speechConfigRef.current = sdk.SpeechConfig.fromSubscription(
            speech_key,
            speech_region
        );
        
        speechConfigRef.current.speechSynthesisVoiceName = 'en-US-AriaNeural';
        speechConfigRef.current.speechSynthesisOutputFormat = 
            sdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3;
        
        synthesizerRef.current = new sdk.SpeechSynthesizer(
            speechConfigRef.current
        );

        return () => {
            if (synthesizerRef.current) {
                synthesizerRef.current.close();
            }
        };
    }, []);

    async function process() {
        if (speechText && synthesizerRef.current) {
            trackPromise(speechApi(speechText));
        }
    }

    async function speechApi(text: string): Promise<void> {
        return new Promise((resolve, reject) => {
            if (!synthesizerRef.current) {
                reject(new Error('Speech synthesizer not initialized'));
                return;
            }

            synthesizerRef.current.speakTextAsync(
                text,
                result => {
                    if (result.reason === sdk.ResultReason.SynthesizingAudioCompleted) {
                        console.log('Speech synthesis completed');
                        // Audio is automatically played by the SDK
                        resolve();
                    } else {
                        reject(new Error('Speech synthesis failed'));
                    }
                },
                error => {
                    console.error('Speech synthesis error:', error);
                    reject(error);
                }
            );
        });
    }

    const updateText = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSpeechText(e.target.value);
    };

    return (
        <div className="pageContainer">
            <h2>Speech</h2>
            <p>Enter text below to hear it spoken aloud using Azure Speech Services.</p>
            <div>
                <input 
                    type="text" 
                    placeholder="(enter some text to be read aloud)" 
                    value={speechText}
                    onChange={updateText}
                    style={{ width: '300px', marginRight: '10px' }}
                />
                <button onClick={process} disabled={!speechText || promiseInProgress}>
                    Read
                </button>
                <br />
                {promiseInProgress && <span>Processing speech...</span>}
            </div>
        </div>
    );
};

export default Page;
```

</details>
</details>
</details>

## Accessibility Considerations

### Screen Reader Compatibility
```typescript
// Announce when speech starts/ends
const announceToScreenReader = (message: string) => {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.textContent = message;
    document.body.appendChild(announcement);
    setTimeout(() => document.body.removeChild(announcement), 1000);
};
```

### Keyboard Navigation
```typescript
const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && speechText) {
        process();
    }
    if (event.key === 'Escape') {
        // Stop current speech
        synthesizerRef.current?.close();
    }
};
```

### Voice Control Options
- Pause/Resume functionality
- Speed control (slow, normal, fast)
- Volume adjustment
- Voice selection (male/female, different accents)

## Real-World Applications

### Retail Environments
- Product information announcements
- Store navigation assistance
- Promotional content delivery
- Accessibility for visually impaired customers

### Customer Service
- Automated phone responses
- Kiosk voice guidance
- Multi-language support
- Queue management announcements

### E-learning and Training
- Course content narration
- Interactive tutorials
- Assessment feedback
- Language learning pronunciation

## Advanced Features

### Speech-to-Text Integration
```typescript
// Add speech recognition for voice input
const recognizer = new sdk.SpeechRecognizer(speechConfig);
recognizer.recognizeOnceAsync(result => {
    setSpeechText(result.text);
});
```

### Emotion and Style Control
```typescript
const ssmlWithEmotion = `
<speak version="1.0" xml:lang="en-US">
    <voice name="en-US-AriaNeural">
        <mstts:express-as style="cheerful">
            Welcome to our amazing store!
        </mstts:express-as>
    </voice>
</speak>`;
```

### Batch Processing
```typescript
async function speakMultipleTexts(texts: string[]) {
    for (const text of texts) {
        await speechApi(text);
        await new Promise(resolve => setTimeout(resolve, 1000)); // Pause between texts
    }
}
```

## Best Practices

### Performance
- Cache frequently used audio
- Implement proper cleanup for audio resources
- Use appropriate audio formats for different devices
- Implement streaming for long texts

### User Experience
- Provide visual feedback during speech processing
- Allow users to interrupt or skip speech
- Offer playback controls (pause, resume, stop)
- Support keyboard shortcuts

### Security and Privacy
- Don't log or store spoken content
- Implement rate limiting
- Validate input text for appropriate content
- Use secure connections for API calls

## Integration Opportunities

1. **Chatbot Integration**: Add voice responses to chat interactions
2. **Notification Systems**: Speak important alerts and updates
3. **Workflow Automation**: Voice-guided step-by-step processes
4. **Multilingual Support**: Combine with translation for global accessibility

## Next Steps

1. Move on to Tutorial 5: SEO Content Generation
2. Explore speech-to-text for voice input
3. Build voice-controlled interfaces
4. Implement conversation systems with speech

## Additional Resources

- [Azure Speech Services Documentation](https://docs.microsoft.com/azure/cognitive-services/speech-service/)
- [Speech SDK for JavaScript](https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstarts/setup-platform?pivots=programming-language-javascript)
- [SSML Reference](https://docs.microsoft.com/azure/cognitive-services/speech-service/speech-synthesis-markup)
- [Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/Understanding/)
