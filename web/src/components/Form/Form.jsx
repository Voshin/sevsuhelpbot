import React, { useCallback, useEffect, useState } from "react";
import { useTelegram } from "../../hooks/useTelegram";
import "./Form.css";

export const Form = () => {
  const [university, setUniversity] = useState("Институт 1");
  const [group, setGroup] = useState("Группа 1 института 1");
  const [extraGroup, setExtraGroup] = useState("");
  const [surname, setSurname] = useState("");
  const [name, setName] = useState("");
  const [patronymic, setPatronymic] = useState("");
  const [location, setLocation] = useState(
    "В главном корпусе (Университетская, 33)"
  );
  const [extraLocation, setExtraLocation] = useState("");

  const universities = new Map();
  universities.set("Институт 1", [
    "Группа 1 института 1",
    "Группа 2 института 1",
    "Группа 3 института 1",
    "Группа 4 института 1",
    "Группа 5 института 1",
    "Группа 6 института 1",
    "Другая",
  ]);
  universities.set("Институт 2", [
    "Группа 1 института 2",
    "Группа 2 института 2",
    "Группа 3 института 2",
    "Группа 4 института 2",
    "Группа 5 института 2",
    "Группа 6 института 2",
    "Другая",
  ]);
  universities.set("Институт 3", [
    "Группа 1 института 3",
    "Группа 2 института 3",
    "Группа 3 института 3",
    "Группа 4 института 3",
    "Группа 5 института 3",
    "Группа 6 института 3",
    "Другая",
  ]);

  const keys = [...universities.keys()];

  const locations = [
    "В главном корпусе (Университетская, 33)",
    "В главном учебном корпусе (Курчатова, 7)",
    "В общежитии 1",
    "В общежитии 2",
    "В общежитии 5",
    "В общежитии 6",
    "В общежитии 7",
    "Дома",
    "Другое",
  ];

  const { tg } = useTelegram();

  const onSendData = useCallback(() => {
    // TODO
    const data = {
      university,
      group,
      name,
      surname,
      patronymic,
      location,
    };
    tg.sendData(JSON.stringify(data));
  }, [university, group, name, surname, patronymic, location]);

  useEffect(() => {
    tg.onEvent("mainButtonClicked", onSendData);
    return () => {
      tg.offEvent("mainButtonClicked", onSendData);
    };
  }, [onSendData]);

  useEffect(() => {
    tg.MainButton.setParams({
      text: "Отправить данные",
    });
  }, []);

  useEffect(() => {
    if (
      !university ||
      !group ||
      !name ||
      !surname ||
      !patronymic ||
      !location
    ) {
      tg.MainButton.hide();
    } else {
      tg.MainButton.show();
    }
  }, [
    university,
    group,
    name,
    surname,
    patronymic,
    location,
    extraGroup,
    extraLocation,
  ]);

  const onChangeUniversity = (e) => {
    setUniversity(e.target.value);
  };

  const onChangeGroup = (e) => {
    setGroup(e.target.value);
  };

  const onChangeExtraGroup = (e) => {
    setExtraGroup(e.target.value);
  };

  const onChangeSurname = (e) => {
    setSurname(e.target.value);
  };

  const OnChangeName = (e) => {
    setName(e.target.value);
  };

  const OnChangePatronymic = (e) => {
    setPatronymic(e.target.value);
  };

  const onChangeLocation = (e) => {
    setLocation(e.target.value);
  };

  const onChangeExtraLocation = (e) => {
    setExtraLocation(e.target.value);
  };

  return (
    <div className={"form"}>
      <h3>Введите ваши данные</h3>
      <span className={"hint"}>Выберите институт</span>
      <select
        value={university}
        onChange={onChangeUniversity}
        className={"select"}
      >
        {keys.map((name, index) => {
          return <option key={index}>{name}</option>;
        })}
      </select>
      <span className={"hint"}>Выберите группу</span>
      <select value={group} onChange={onChangeGroup} className={"select"}>
        {universities.get(university).map((name, index) => {
          return <option key={index}>{name}</option>;
        })}
      </select>
      {group === "Другая" && (
        <input
          className={"input"}
          type="text"
          placeholder={"Введите группу"}
          value={extraGroup}
          onChange={onChangeExtraGroup}
        />
      )}
      <input
        className={"input"}
        type="text"
        placeholder={"Фамилия"}
        value={surname}
        onChange={onChangeSurname}
      />
      <input
        className={"input"}
        type="text"
        placeholder={"Имя"}
        value={name}
        onChange={OnChangeName}
      />
      <input
        className={"input"}
        type="text"
        placeholder={"Отчество"}
        value={patronymic}
        onChange={OnChangePatronymic}
      />
      <span className={"hint"}>Выберите свое местоположение</span>
      <select value={location} onChange={onChangeLocation} className={"select"}>
        {locations.map((location, index) => {
          return <option key={index}>{location}</option>;
        })}
      </select>
      {location === "Другое" && (
        <input
          className={"input"}
          type="text"
          placeholder={"Введите местоположение"}
          value={extraLocation}
          onChange={onChangeExtraLocation}
        />
      )}
    </div>
  );
};
