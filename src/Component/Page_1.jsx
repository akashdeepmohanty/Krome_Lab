import React, { useState } from "react";
import Edit from "./Edit";
import Button from "./Button";

const Page_1 = ({ fileRef, file, message, setMessage, BClick, FileChange, EXDownload, tempo ,setTempo, pitch, setPitch, tempoOrignal, setTempoOrignal  }) => {


  const EXProcess = async () => {
    const res = await fetch("http://localhost:5000/process", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        tempo: tempo,
        tempoOrignal:tempoOrignal,
        pitch: pitch,
      }),
    });

    const data = await res.json();
    setMessage(data.message);
  };

  return (
    <>
      <main className="bg-[url(4536.jpg)] bg-cover">
        <div className=" mx-25 my-5">
          <div className=" p-5 rounded-3xl bg-black/50 text-purple-950 text-4xl font-bold text-center ">
            <h1 className="font-Nunito text-6xl font-bold text-white">
              Krome Lab
            </h1>
          </div>

          <div className=" p-5 my-5 rounded-3xl bg-black/50 text-black">
            <Edit
              fileRef={fileRef}
              file={file}
              message={message}
              setMessage={setMessage}
              BClick={BClick}
              FileChange={FileChange}
              tempo={tempo}
              setTempo={setTempo}
              pitch={pitch}
              setPitch={setPitch}
              tempoOrignal={tempoOrignal}
              settempoOrignal={setTempoOrignal}
            />
          </div>
          <div className=" p-5 my-5 rounded-3xl bg-black/50 text-black">
            <Button EXDownload={EXDownload} EXProcess={EXProcess} file={file} />
          </div>
        </div>
      </main>
    </>
  );
};

export default Page_1;
