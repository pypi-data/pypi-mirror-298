export function formToJson(form: any, extraParams: object = {}): string {
    // Create a FormData object from the form
    const formData = new FormData(form);
    // Convert the FormData object to a plain object
    const formObject: any = {};
    formData.forEach((value, key) => {
        formObject[key] = value;
    });
    Object.entries(extraParams).forEach(([key, value]) => {
        formObject[key] = value;
    });
    // Convert the form object to JSON
    return JSON.stringify(formObject);
}
