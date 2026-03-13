import UploadBox from "../components/UploadBox";
import PersonaSelector from "../components/PersonaSelector";
import SummaryPanel from "../components/SummaryPanel";
import ChatWidget from "../components/ChatWidget";

function Home() {
  return (
    <div className="grid grid-cols-2 gap-6">
      <div>
        <UploadBox />
        <PersonaSelector />
      </div>

      <div>
        <SummaryPanel />
        <ChatWidget />
      </div>
    </div>
  );
}

export default Home;
