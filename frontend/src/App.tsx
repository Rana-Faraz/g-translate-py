import { useState } from "react";
import { Textarea } from "./components/ui/textarea";
import { Button } from "./components/ui/button";

const BASE_URL = import.meta.env.VITE_BASE_URL;

function App() {
  const [text, setText] = useState<string>("");
  const [translatedText, setTranslatedText] = useState<string>("");

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const response = await fetch(`${BASE_URL}/translate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: text,
    });

    const data = await response.json();
    setTranslatedText(data.ar);
    console.log(data);
  };
  return (
    <div className="space-y-8">
      <form
        onSubmit={handleSubmit}
        className="container mx-auto min-h-screen flex flex-col gap-4  py-16 "
      >
        <Textarea
          name="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type something..."
          rows={10}
        />
        <Button type="submit" className="mt-4 w-max">
          Submit
        </Button>
      </form>
      <div className="container mx-auto">
        {translatedText && (
          <div className="p-4 bg-gray-100 rounded-md">
            <h2 className="text-lg font-bold">Translated Text</h2>
            <p>{JSON.stringify(translatedText)}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
