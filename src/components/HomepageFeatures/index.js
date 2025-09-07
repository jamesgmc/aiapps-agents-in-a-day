import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: '🤖 Build AI Agents',
    icon: '🤖',
    description: (
      <>
        Learn to create intelligent AI agents that can reason, plan, and take actions
        autonomously. From simple chatbots to complex agentic systems.
      </>
    ),
  },
  {
    title: '⚡ Rapid Development',
    icon: '⚡',
    description: (
      <>
        Get hands-on experience building AI apps in just one day using modern
        frameworks, Azure OpenAI, and cutting-edge agentic design patterns.
      </>
    ),
  },
  {
    title: '🎯 Real-World Labs',
    icon: '🎯',
    description: (
      <>
        Practice with interactive labs covering LLM integration, RAG systems,
        chatbots, and multi-agent workflows that you can apply immediately.
      </>
    ),
  },
];

function Feature({icon, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <div className="ai-icon">
          {icon}
        </div>
      </div>
      <div className="text--center padding-horiz--md ai-feature-card">
        <h3 style={{
          background: 'linear-gradient(135deg, #2563eb 0%, #e935c7 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          fontWeight: '600',
          fontSize: '1.5rem',
          marginBottom: '1rem'
        }}>{title}</h3>
        <p style={{
          fontSize: '1.1rem',
          lineHeight: '1.6',
          color: 'var(--ifm-color-emphasis-800)'
        }}>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div style={{
          textAlign: 'center',
          marginBottom: '4rem'
        }}>
          <h2 style={{
            fontSize: '2.5rem',
            fontWeight: '700',
            background: 'linear-gradient(135deg, #2563eb 0%, #e935c7 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            marginBottom: '1rem'
          }}>
            Master AI Agents in One Day 🚀
          </h2>
          <p style={{
            fontSize: '1.25rem',
            color: 'var(--ifm-color-emphasis-700)',
            maxWidth: '600px',
            margin: '0 auto'
          }}>
            Join our intensive workshop to learn agentic design patterns, build intelligent AI applications, 
            and deploy real-world solutions using the latest technologies.
          </p>
        </div>
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
