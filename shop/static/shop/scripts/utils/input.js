export const handlePasswordToggle = (input, callback) => {

    if (!input) return;

    callback(input.type === "password" ? "text" : "password");

};

