import PromptForm from './components/PromptForm';


function App() {
  return (
    <div className="app-container">
      <img
    src="/images/bg-orange.png"
    className="absolute inset-0 w-full h-full object-cover opacity-10 pointer-events-none z-0"
    alt="lines background"
  />
      <header className="app-header">
        <h1 className="app-title">Narrative Space</h1>

        <p className="app-subtitle">Generative AI for Architectural Narratives</p>
      </header>

      <main className ="app-main">
        <PromptForm />
      </main>
    </div>
  );
}

export default App;

