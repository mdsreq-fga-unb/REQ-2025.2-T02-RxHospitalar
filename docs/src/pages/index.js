import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import {ArrowRight, ExternalLink} from 'lucide-react'; // precisa instalar lucide-react

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx(styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent}>
          <div className={styles.textSection}>
            <h1 className={styles.title}>{siteConfig.title}</h1>
            <p className={styles.subtitle}>{siteConfig.tagline}</p>
            <div className={styles.buttons}>
              <Link className={styles.primaryButton} to="/docs/intro">
                Documentação <ArrowRight size={16} className={styles.iconRight}/>
              </Link>
              <Link className={styles.secondaryButton} href="https://github.com/mdsreq-fga-unb/REQ-2025.2-T02-RxHospitalar">
                GitHub <ExternalLink size={16} className={styles.iconRight}/>
              </Link>
            </div>
          </div>
          <div className={styles.imageSection}>
            <img src="img/logo-grupo.png" alt="Logo do Projeto" className={styles.heroImage} />
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Página inicial do projeto">
      <HomepageHeader />
    </Layout>
  );
}