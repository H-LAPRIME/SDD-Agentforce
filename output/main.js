const { useState, useEffect, useRef } = React;

// --- Composants UI réutilisables ---

const Button = ({ children, variant = 'primary', className = '', ...props }) => {
  const baseStyle = "inline-flex items-center justify-center px-6 py-3 border text-base font-medium rounded-lg transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2";
  const variants = {
    primary: "border-transparent text-white bg-brand-600 hover:bg-brand-700 shadow-lg hover:shadow-xl focus:ring-brand-500",
    secondary: "border-transparent text-brand-700 bg-brand-100 hover:bg-brand-200 focus:ring-brand-500",
    outline: "border-slate-300 text-slate-700 bg-white hover:bg-slate-50 focus:ring-brand-500",
    ghost: "border-transparent text-slate-600 hover:text-brand-600 hover:bg-brand-50"
  };

  return (
    <button className={`${baseStyle} ${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
};

const SectionTitle = ({ title, subtitle, light = false }) => (
  <div className="text-center max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 mb-16">
    <h2 className={`text-3xl md:text-4xl font-extrabold ${light ? 'text-white' : 'text-slate-900'} tracking-tight mb-4`}>
      {title}
    </h2>
    <p className={`text-lg ${light ? 'text-slate-300' : 'text-slate-600'}`}>
      {subtitle}
    </p>
  </div>
);

const Card = ({ icon: Icon, title, description }) => (
  <div className="bg-white p-8 rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border border-slate-100 group">
    <div className="w-12 h-12 bg-brand-100 rounded-lg flex items-center justify-center mb-6 group-hover:bg-brand-600 transition-colors duration-300">
      <Icon className="w-6 h-6 text-brand-600 group-hover:text-white transition-colors duration-300" />
    </div>
    <h3 className="text-xl font-bold text-slate-900 mb-3">{title}</h3>
    <p className="text-slate-600 leading-relaxed">{description}</p>
  </div>
);

const PricingCard = ({ title, price, features, recommended = false }) => (
  <div className={`relative bg-white rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 flex flex-col h-full ${recommended ? 'border-2 border-brand-500 ring-4 ring-brand-500/20 transform md:-translate-y-4' : 'border border-slate-100'}`}>
    {recommended && (
      <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gradient-to-r from-brand-600 to-blue-500 text-white px-4 py-1 rounded-full text-sm font-bold tracking-wide uppercase shadow-md">
        Populaire
      </div>
    )}
    <div className="p-8 flex-1">
      <h3 className="text-xl font-semibold text-slate-900 mb-2">{title}</h3>
      <div className="flex items-baseline mb-6">
        <span className="text-4xl font-extrabold text-slate-900">{price}</span>
        {price !== 'Gratuit' && <span className="text-slate-500 ml-2">/mois</span>}
      </div>
      <ul className="space-y-4 mb-8">
        {features.map((feature, idx) => (
          <li key={idx} className="flex items-start">
            <svg className={`flex-shrink-0 w-5 h-5 mr-3 ${recommended ? 'text-brand-500' : 'text-slate-400'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span className="text-slate-600">{feature}</span>
          </li>
        ))}
      </ul>
    </div>
    <div className="p-8 bg-slate-50 rounded-b-2xl border-t border-slate-100">
      <Button variant={recommended ? 'primary' : 'outline'} className="w-full">
        {recommended ? 'Commencer maintenant' : 'Essayer gratuitement'}
      </Button>
    </div>
  </div>
);

const AccordionItem = ({ question, answer, isOpen, onClick }) => (
  <div className="border-b border-slate-200 last:border-0">
    <button 
      className="w-full flex justify-between items-center py-6 text-left focus:outline-none group"
      onClick={onClick}
      aria-expanded={isOpen}
    >
      <span className={`text-lg font-medium transition-colors duration-300 ${isOpen ? 'text-brand-600' : 'text-slate-900 group-hover:text-brand-600'}`}>
        {question}
      </span>
      <svg 
        className={`w-5 h-5 text-slate-500 transition-transform duration-300 ${isOpen ? 'rotate-180 text-brand-600' : ''}`} 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
      </svg>
    </button>
    <div 
      className={`overflow-hidden transition-all duration-300 ease-in-out ${isOpen ? 'max-h-96 opacity-100 mb-6' : 'max-h-0 opacity-0'}`}
    >
      <p className="text-slate-600 leading-relaxed">{answer}</p>
    </div>
  </div>
);

// --- Icônes SVG ---
const Icons = {
  Chart: (props) => <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" {...props}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>,
  Zap: (props) => <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" {...props}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>,
  Shield: (props) => <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" {...props}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>,
  Cpu: (props) => <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" {...props}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>,
  Check: (props) => <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" {...props}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>,
  Menu: (props) => <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" {...props}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" /></svg>,
  X: (props) => <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" {...props}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>,
  ChevronDown: (props) => <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" {...props}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>,
  Facebook: (props) => <svg fill="currentColor" viewBox="0 0 24 24" {...props}><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg>,
  Twitter: (props) => <svg fill="currentColor" viewBox="0 0 24 24" {...props}><path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z"/></svg>,
  Linkedin: (props) => <svg fill="currentColor" viewBox="0 0 24 24" {...props}><path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/></svg>,
};

// --- Composant Principal App ---

const App = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [openFaqIndex, setOpenFaqIndex] = useState(0);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const features = [
    {
      icon: Icons.Chart,
      title: "Analyses Prédictives",
      description: "Nous utilisons des algorithmes avancés pour anticiper les tendances du marché et optimiser votre croissance."
    },
    {
      icon: Icons.Zap,
      title: "Automatisation Intelligente",
      description: "Éliminez les tâches répétitives. AtlasFlow orchestre vos processus métiers avec une précision chirurgicale."
    },
    {
      icon: Icons.Shield,
      title: "Sécurité Enterprise",
      description: "Vos données sont protégées par des normes de cryptage de pointe, conformes aux régulations RGPD et SOC2."
    },
    {
      icon: Icons.Cpu,
      title: "Intégration API",
      description: "Connectez AtlasFlow à votre stack existante en quelques minutes grâce à notre API RESTful ultra-performante."
    }
  ];

  const pricingPlans = [
    {
      title: "Starter",
      price: "49€",
      features: ["Utilisateurs illimités", "Analyses de base", "Support par email", "Stockage 50GB"],
      recommended: false
    },
    {
      title: "Professionnel",
      price: "129€",
      features: ["Tout de Starter", "Analyses prédictives", "API Access", "Support prioritaire 24/7", "Stockage 500GB"],
      recommended: true
    },
    {
      title: "Entreprise",
      price: "Sur devis",
      features: ["Solutions sur mesure", "Dédié Infrastructure", "SLA 99.99%", "Compte manager dédié", "Formation personnalisée"],
      recommended: false
    }
  ];

  const faqs = [
    {
      question: "Puis-je migrer mes données depuis mon ancien outil ?",
      answer: "Absolument. Nous proposons un service de migration assistée qui permet d'importer vos données en toute sécurité sans interruption de service."
    },
    {
      question: "Y a-t-il une période d'essai gratuite ?",
      answer: "Oui, nous offrons 14 jours d'essai gratuit sur le plan Professionnel, sans carte bancaire requise."
    },
    {
      question: "Le contrat est-il engageant ?",
      answer: "Non, aucun engagement à long terme. Vous pouvez résilier votre abonnement à tout moment avec un préavis de 7 jours."
    },
    {
      question: "Proposez-vous des tarifs pour les startups ?",
      answer: "Nous avons un programme spécial 'Startup' qui offre une réduction de 30% durant les 12 premiers mois pour les entreprises en forte croissance."
    }
  ];

  return (
    <div className="min-h-screen font-sans bg-slate-50 selection:bg-brand-500 selection:text-white">
      
      {/* Navigation */}
      <nav className={`fixed w-full z-50 transition-all duration-300 ${scrolled ? 'bg-white/95 backdrop-blur-md shadow-md py-4' : 'bg-transparent py-6'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <span className={`text-2xl font-extrabold tracking-tighter ${scrolled ? 'text-slate-900' : 'text-white'}`}>
                Atlas<span className="text-brand-500">Flow</span>
              </span>
            </div>
            
            {/* Desktop Menu */}
            <div className="hidden md:flex items-center space-x-8">
              {['Fonctionnalités', 'Tarifs', 'FAQ', 'Contact'].map((item) => (
                <a 
                  key={item} 
                  href={`#${item.toLowerCase()}`} 
                  className={`text-sm font-medium hover:text-brand-500 transition-colors ${scrolled ? 'text-slate-600' : 'text-slate-200'}`}
                >
                  {item}
                </a>
              ))}
              <Button variant={scrolled ? 'primary' : 'secondary'} className="py-2 px-4 text-sm">
                Connexion
              </Button>
            </div>

            {/* Mobile Menu Button */}
            <div className="md:hidden">
              <button 
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className={`p-2 rounded-md ${scrolled ? 'text-slate-600' : 'text-white'}`}
                aria-label="Menu"
              >
                {isMobileMenuOpen ? <Icons.X className="w-6 h-6" /> : <Icons.Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Menu Dropdown */}
        {isMobileMenuOpen && (
          <div className="md:hidden absolute top-full left-0 w-full bg-white border-b border-slate-200 shadow-lg animate-in slide-in-from-top-5 duration-200">
            <div className="px-4 py-6 space-y-4 flex flex-col">
              {['Fonctionnalités', 'Tarifs', 'FAQ', 'Contact'].map((item) => (
                <a 
                  key={item} 
                  href={`#${item.toLowerCase()}`}
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="text-base font-medium text-slate-600 hover:text-brand-600 py-2 border-b border-slate-50"
                >
                  {item}
                </a>
              ))}
              <Button variant="primary" className="w-full mt-4">Actionner</Button>
            </div>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <header className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden">
        {/* Background Image with Overlay */}
        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 bg-gradient-to-r from-slate-900 via-slate-900 to-brand-900 mix-blend-multiply z-10 opacity-95"></div>
          <img 
            src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" 
            alt="Dashboard Analytics" 
            className="w-full h-full object-cover"
          />
        </div>

        <div className="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center px-3 py-1 rounded-full bg-brand-500/20 border border-brand-400/30 backdrop-blur-sm mb-8 animate-bounce-slow">
            <span className="text-brand-300 text-xs font-bold uppercase tracking-widest mr-2">Nouveau</span>
            <span className="text-brand-100 text-sm">Version 2.0 désormais disponible</span>
          </div>
          
          <h1 className="text-4xl sm:text-5xl lg:text-7xl font-extrabold text-white tracking-tight mb-8 leading-tight">
            Piloter la croissance de votre <br className="hidden sm:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-400 to-cyan-300">SaaS</span> n'a jamais été aussi simple.
          </h1>
          
          <p className="mt-4 max-w-2xl mx-auto text-xl text-slate-300 mb-10 font-light">
            AtlasFlow centralise vos données, automatise vos flux de travail et propulse votre entreprise vers de nouveaux sommets grâce à l'IA.
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Button variant="primary" className="w-full sm:w-auto text-lg px-8 py-4">
              Commencer gratuitement
            </Button>
            <Button variant="outline" className="w-full sm:w-auto text-lg px-8 py-4 bg-transparent text-white border-white hover:bg-white hover:text-slate-900">
              Démo en direct
            </Button>
          </div>

          {/* Hero Image Mockup */}
          <div className="mt-16 relative mx-auto max-w-5xl">
            <div className="rounded-xl bg-slate-800/50 p-2 backdrop-blur-sm border border-slate-700 shadow-2xl">
              <img 
                src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&auto=format&fit=crop&w=2426&q=80" 
                alt="Interface AtlasFlow" 
                className="rounded-lg w-full h-auto opacity-90"
              />
            </div>
            {/* Floating Elements */}
            <div className="absolute -top-6 -right-6 bg-white p-4 rounded-xl shadow-xl hidden md:block animate-float">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-green-100 rounded-full">
                  <Icons.Zap className="w-5 h-5 text-green-600" />
                </div>
                <div>
                  <p className="text-xs text-slate-500 font-medium">Croissance</p>
                  <p className="text-lg font-bold text-slate-900">+124%</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Features Section */}
      <section id="fonctionnalités" className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionTitle 
            title="Tout ce dont vous avez besoin" 
            subtitle="Une suite complète d'outils puissants conçus pour scalabilité et efficacité."
          />
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} {...feature} />
            ))}
          </div>

          {/* Feature Showcase */}
          <div className="mt-24 bg-slate-50 rounded-3xl overflow-hidden">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div className="p-8 lg:p-16 order-2 lg:order-1">
                <h3 className="text-3xl font-bold text-slate-900 mb-6">Tableau de bord unifié</h3>
                <p className="text-lg text-slate-600 mb-6 leading-relaxed">
                  Visualisez l'ensemble de vos KPIs en temps réel. Notre interface intuitive vous permet de créer des rapports personnalisés en quelques secondes, sans avoir besoin de connaissances techniques.
                </p>
                <ul className="space-y-4 mb-8">
                  {['Suivi des revenus en temps réel', 'Analyse de rétention des clients', 'Rapports automatisés par email'].map((item, i) => (
                    <li key={i} className="flex items-center text-slate-700">
                      <div className="w-6 h-6 rounded-full bg-brand-100 flex items-center justify-center mr-3">
                        <svg className="w-4 h-4 text-brand-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                      </div>
                      {item}
                    </li>
                  ))}
                </ul>
                <Button variant="secondary">Découvrir le dashboard</Button>
              </div>
              <div className="order-1 lg:order-2 relative h-full min-h-[400px]">
                <img 
                  src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80" 
                  alt="Dashboard UI" 
                  className="absolute inset-0 w-full h-full object-cover rounded-none lg:rounded-l-3xl shadow-2xl"
                  loading="lazy"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-brand-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center divide-x divide-brand-700/50">
            {[
              { label: "Clients actifs", value: "2,500+" },
              { label: "Revenus générés", value: "$50M+" },
              { label: "Pays couverts", value: "45" },
              { label: "Uptime garanti", value: "99.9%" }
            ].map((stat, index) => (
              <div key={index} className="p-4">
                <div className="text-4xl md:text-5xl font-extrabold text-brand-400 mb-2">{stat.value}</div>
                <div className="text-brand-100 font-medium">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="tarifs" className="py-24 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionTitle 
            title="Des tarifs simples et transparents" 
            subtitle="Choisissez le plan qui correspond à votre stade de croissance."
          />
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {pricingPlans.map((plan, index) => (
              <PricingCard key={index} {...plan} />
            ))}
          </div>
          
          <p className="text-center text-slate-500 mt-8 text-sm">
            Tous les prix sont TTC. Paiement mensuel ou annuel (2 mois offerts).
          </p>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="py-24 bg-white">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionTitle 
            title="Questions Fréquentes" 
            subtitle="Vous avez des questions ? Nous avons les réponses."
          />
          
          <div className="space-y-2">
            {faqs.map((faq, index) => (
              <AccordionItem 
                key={index}
                question={faq.question}
                answer={faq.answer}
                isOpen={openFaqIndex === index}
                onClick={() => setOpenFaqIndex(openFaqIndex === index ? -1 : index)}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-24 bg-slate-50 relative overflow-hidden">
        <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-brand-100 rounded-full blur-3xl opacity-50"></div>
        <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-96 h-96 bg-purple-100 rounded-full blur-3xl opacity-50"></div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div className="grid lg:grid-cols-2">
              <div className="p-10 md:p-16 bg-brand-600 text-white flex flex-col justify-between">
                <div>
                  <h2 className="text-3xl font-bold mb-6">Discutons de votre projet</h2>
                  <p className="text-brand-100 mb-8 leading-relaxed">
                    Notre équipe d'experts est prête à vous accompagner. Que ce soit pour une intégration personnalisée ou une démo, nous sommes à votre écoute.
                  </p>
                  
                  <div className="space-y-6">
                    <div className="flex items-center">
                      <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center mr-4">
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                      </div>
                      <span>contact@atlasflow.io</span>
                    </div>
                    <div className="flex items-center">
                      <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center mr-4">
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                      </div>
                      <span>123 Avenue de l'Innovation, Paris</span>
                    </div>
                  </div>
                </div>
                
                <div className="mt-12 flex space-x-4">
                  {[Icons.Twitter, Icons.Linkedin, Icons.Facebook].map((Icon, i) => (
                    <a key={i} href="#" className="w-10 h-10 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors">
                      <Icon className="w-5 h-5 text-white" />
                    </a>
                  ))}
                </div>
              </div>
              
              <div className="p-10 md:p-16 bg-white">
                <form className="space-y-6" onSubmit={(e) => e.preventDefault()}>
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-slate-700 mb-1">Nom complet</label>
                    <input type="text" id="name" className="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all" placeholder="Jean Dupont" required />
                  </div>
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-1">Email professionnel</label>
                    <input type="email" id="email" className="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all" placeholder="jean@entreprise.com" required />
                  </div>
                  <div>
                    <label htmlFor="message" className="block text-sm font-medium text-slate-700 mb-1">Message</label>
                    <textarea id="message" rows="4" className="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all" placeholder="Comment pouvons-nous vous aider ?" required></textarea>
                  </div>
                  <Button type="submit" variant="primary" className="w-full">Envoyer le message</Button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-300 py-16 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-8 mb-12">
            <div className="col-span-2 lg:col-span-2">
              <span className="text-2xl font-extrabold tracking-tighter text-white mb-4 block">
                Atlas<span className="text-brand-500">Flow</span>
              </span>
              <p className="text-slate-400 max-w-xs mb-6">
                La plateforme tout-en-un pour piloter, analyser et scaler votre entreprise SaaS moderne.
              </p>
              <p className="text-sm text-slate-500">© 2023 AtlasFlow Inc. Tous droits réservés.</p>
            </div>
            
            <div>
              <h4 className="text-white font-bold mb-4">Produit</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-brand-400 transition-colors">Fonctionnalités</a></li>
                <li><a href="#" className="hover:text-brand-400 transition-colors">Intégrations</a></li>
                <li><a href="#" className="hover:text-brand-400 transition-colors">Tarifs</a></li>
                <li><a href="#" className="hover:text-brand-400 transition-colors">Changelog</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-white font-bold mb-4">Ressources</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-brand-400 transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-brand-400 transition-colors">API</a></li>
                <li><a href="#" className="hover:text-brand-400 transition-colors">Guide développeur</a></li>
                <li><a href="#" className="hover:text-brand-400 transition-colors">Blog</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-white font-bold mb-4">Société</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-brand-400 transition-colors">À propos</a></li>
                <li><a href="#" className="hover:text-brand-400 transition-colors">Carrières</a></li>
                <li><a href="#" className="hover:text-brand-400 transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-brand-400 transition-colors">Mentions légales</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-slate-800 pt-8 flex flex-col md:flex-row justify-between items-center">
             <div className="flex space-x-6 mb-4 md:mb-0">
               <a href="#" className="text-slate-500 hover:text-white transition-colors">Confidentialité</a>
               <a href="#" className="text-slate-500 hover:text-white transition-colors">CGU</a>
               <a href="#" className="text-slate-500 hover:text-white transition-colors">Sécurité</a>
             </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);