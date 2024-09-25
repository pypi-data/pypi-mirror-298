import re

class Opt:
    def __init__(
        self,
        name_action,
        endpoint_name,
        htmlclass="btn btn-primary btn-sm",
        isPostId=False,
        isPostRow=False,
        isGetRow=False,
        isGetId=False,
    ):
        self.name_action = name_action
        self.htmlclass = htmlclass
        self.endpoint_name = endpoint_name
        self.isPostId = isPostId
        self.isPostRow = isPostRow
        self.isGetRow = isGetRow
        self.isGetId = isGetId

    def toMetaData(self):
        Opt = {
            "name_action":self.name_action,
            "endpoint_name":self.endpoint_name,
            "class": self.htmlclass,
        }
        if self.isPostId:
            Opt["isPostId"] = True
        if self.isPostRow:
            Opt["isPostRow"] = True
        if self.isGetId:
            Opt["isGetId"] = True
        if self.isGetRow:
            Opt["isGetRow"] = True
        return Opt


class Btn:
    def __init__(
        self,
        name_action,
        endpoint_name=None,
        htmlclass="btn btn-primary btn-sm",
        isSubmit=False,
        isSimple=False,
    ) -> None:
        self.name_action = name_action
        self.endpoint_name = endpoint_name
        self.htmlclass = htmlclass
        self.isSubmit = isSubmit
        self.isSimple = isSimple

    def toMetaData(self):
        Btn = {
            "name_action": self.name_action,
            "endpoint_name": self.endpoint_name,
            "class": self.htmlclass,
        }
        if self.isSubmit:
            Btn["isSubmit"] = True
        if self.isSimple:
            Btn["isSimple"] = True
        return Btn
    
    def copyName(self, newText):
        return Btn(
        name_action = newText,
        endpoint_name=self.endpoint_name,
        htmlclass=self.htmlclass,
        isSubmit=self.isSubmit,
        isSimple=self.isSimple,
        )



def as_natural_words_list(row: dict[str]):
    natural_words = []
    for k in row:
        k = k.replace("_", " ")
        k = k.capitalize()
        natural_words.append(k)
    return natural_words


class BuildViewError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


# def build_inputs(model:CrudEntityModel, id, requireds, enums):
def build_inputs(
    sample: dict[str], data: dict[str] = None, requireds=[], disableds=[], enums={}, enumsmuliple=[]
):
    require_sample = not data
    # date_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
    date_pattern = r'(\d{4}-\d{2}-\d{2})|(\d{2}/\d{2}/\d{4})'
    time_patern = r'([01]\d|2[0-3]):[0-5]\d(:[0-5]\d)?'
    datetime_pattern = r'(\d{4}-\d{2}-\d{2} [01]\d:[0-5]\d(:[0-5]\d)?)|(\d{2}/\d{2}/\d{4} [01]\d:[0-5]\d(:[0-5]\d)?)'
    telf_pattern = "[0-9]{10}"
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'    
    int_pattern = "[-]{0,1}[0-9]+"
    float_pattern = r"[-]{0,1}[0-9]+\.[0-9]+"
    print("---------- build_inputs.sample")
    print(sample)
    print("---------- build_inputs.data")
    print(data)
    if not data and not sample:
        raise BuildViewError("Se requiere al menos el data o sample.")
    if not data:
        data = sample
    if not data:
        data = sample
    inps = []
    vals_default_forms = {}
    label_form = {}
    for k, v in sample.items():
        v = str(v)
        inp = {}
        inp["label"] = k.capitalize().replace("_", " ")
        label_form[k] = inp["label"]
        inp["name"] = k
        inp["required"] = k in requireds
        inp["disabled"] = k in disableds
        inp["multiple"] = k in enumsmuliple
        if k in enums:
            inp["type"] = "select"
            enum = enums[k]
            inp["options"] = enum
            if data and data.get(k) is not None and data.get(k) in enum:
                inp["disable"] = data[k]
            else:
                inp["disable"] = sample[k]
        elif "\n" in v:
            inp["type"] = "textarea"
            if require_sample:
                v = ""    
            else:
                v = data.get(k)
        elif re.fullmatch(date_pattern, v):
            inp["type"] = "date"
            if require_sample:
                v = "aaaa-mm-dd"    
            else:
                v = data.get(k)
        elif re.fullmatch(time_patern, v):
            inp["type"] = "time"
            if require_sample:
                v = "HH:MM:ss"    
            else:
                v = data.get(k)
        elif re.fullmatch(datetime_pattern, v):
            inp["type"] = "datetime-local"
            if require_sample:
                v = "aaaa-mm-dd HH:MM:ss"    
            else:
                v = data.get(k)
        elif re.fullmatch(telf_pattern, v):
            inp["type"] = "tel"
            inp["pattern"] = telf_pattern
            if require_sample:
                v = ""
            else:
                v = data.get(k)
        elif re.fullmatch(email_pattern, v):
            inp["type"] = "email"            
            if require_sample:
                v = ""
            else:
                v = data.get(k)
        elif re.fullmatch(int_pattern, v):
            inp["type"] = "number"
            if require_sample:
                v = "0"
            else:
                v = data.get(k)
        elif re.fullmatch(float_pattern, v):
            inp["type"] = "number"
            inp["step"] = "0.01"
            if require_sample:
                v = "0.0"
            else:
                v = data.get(k)
        else:
            inp["type"] = "text"
            if require_sample:
                v = ""
            else:
                v = data.get(k)

        inp["value"] = v
        inps.append(inp)
        vals_default_forms[k] = v
    return (vals_default_forms, inps, label_form)


def requiredsEquals(sample_dict, form_dict, requireds=None):
    if requireds is None:
        requireds = []
    # print("´ñññññññññññññññññññññññññ requiredsEquals ñññññññññññññññññññññññññññ")
    # print("sample_dict: {0}".format(str(sample_dict)))
    # print("form_dict: {0}".format(str(form_dict)))
    # Filtramos solo las claves que están en requireds
    return {
        k: sample_dict[k]
        for k in requireds
        if (k in sample_dict and k in form_dict and sample_dict[k] == form_dict[k])
        or (k in sample_dict and k not in form_dict)
    }


class FormView:
    """
        Ejemplo de uso:
        .. code-block:: python
            userform = FormView(
                model = Usuario(request.form),
                requireds = ["id", "username", "password"],
                enums = { "estado_civil": ["SOLTERO", "VIUDO", "CASADO", "CONCUBINATO"] }
            )
    """
    # Eventos de carga de datos en endpoint
    _endpoint_change_listeners = []
    vals_default_forms = None
    lbl_form = None

    def __init__(
        self,
        entity_name,
        sample,
        colrequireds: list[str],
        coldisableds: list[str],
        enums: dict[str, list[str]],
        text_submit="Enviar",
        text_cancel="Cancelar",
        enumsmuliple={},
        title=None,
        btns={},
    ):
        self.entity_name = entity_name
        self.enumsmuliple = enumsmuliple
        self.sample = sample
        self.requireds = colrequireds
        self.disableds = coldisableds
        self.enums = enums
        self.title = title
        self.text_submit = text_submit
        self.text_cacel = text_cancel
        self.btns:dict[str, Btn] = btns
        self.endpoint_name = None
        self.main_btn =  Btn(
                self.text_submit,
                isSubmit=True,
                htmlclass="btn btn-primary",
            )
        self.cancel_btn = Btn(
                self.text_cacel,
                htmlclass="btn btn-secondary",
                endpoint_name=""
            )

    def setEnpointName(self, endpoint_name):
        self.endpoint_name = endpoint_name
        for listener in FormView._endpoint_change_listeners:
            listener(endpoint_name, self)

    def __defaultTitle(self):
        entity_name = self.entity_name
        if entity_name is None or entity_name.endswith("s"):
            return f"Gestión de {entity_name}"
        if entity_name.endswith("l"):
            return f"Gestión de {entity_name}es."
        if not entity_name.endswith("s"):
            return f"Gestión de {entity_name}s."
        return f"Gestión de {entity_name}"

    def getTitle(self):
        if self.title is None:
            self.title = self.__defaultTitle()
        return self.title
    
    def quitBtns(self):
        self.main_btn = None
        self.cancel_btn = None
        self.btns = {}        

    def anyEqual(self, form_dict):
        print(f"------- DATOS POR COMPARAR: dataform={FormView.vals_default_forms}")
        if not isinstance(form_dict, dict):
            form_dict = dict(form_dict)
        required_equal_data = requiredsEquals(
            FormView.vals_default_forms, form_dict, self.requireds
        )
        if FormView.lbl_form is None:
            FormView.lbl_form = {}
        required_fields = [
            FormView.lbl_form.get(field) for field in required_equal_data
        ]
        FormView.vals_default_forms = None
        return (required_equal_data != {}, ",".join(required_fields))

    def toForm(self, data: dict[str], endpoint_name=None):
        sample = self.sample
        print("--- FormView: data:")
        print(data)
        if endpoint_name:
            self.setEnpointName(endpoint_name)
        newrow = None
        if data is not None:
            if not sample:
                sample = data
            newrow = {}
            for key in sample:
                newrow[key] = data[key]
            print("--- FormView: newrow:")
            print(newrow)
        if newrow:
            viewdata = newrow
        else:
            viewdata = data
        print("--- FormView: SAMPLE:")
        print(self.sample)
        FormView.vals_default_forms, inps, FormView.lbl_form = build_inputs(
            self.sample, viewdata, self.requireds, self.disableds, self.enums, self.enumsmuliple
        )

        btns = []
        if self.btns:
            for kbtn in self.btns:
                btn = self.btns[kbtn]
                btns.append(btn.toMetaData())
        print("---- FORM BTNS ------")
        print(btns)
        print("---- FORM SELF BTNS ------")
        print(self.btns)
        form_data = {
            "title":self.title,
            "inputs": inps,
            "entity_name": self.entity_name,
            "main_btn": self.main_btn.toMetaData() if self.main_btn else None,
            "cancel_btn": self.cancel_btn.toMetaData() if self.cancel_btn else None,
            "btns": btns,
            "data": data,
        }
        return form_data


EditOpt = Opt(
    name_action= "Editar",
    isGetId= True,
    endpoint_name="edit",
    htmlclass="btn btn-warning btn-sm"
)
DeleteOpt = Opt(
    name_action= "Eliminar",
    isPostId= True,
    endpoint_name="delete",
    htmlclass="btn btn-danger btn-sm"
)

class IlegalTableArgument(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class IlegalCrudViewArgument(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnvalidateValueException(Exception):
    def __init__(self, key, value) -> None:
        super().__init__(
            f"Valor necesario ausente en {key}='{value}', puede que {key} no se esté validando en el envío del formulario."
        )

class TableView:
    # def __init__(self, head_names, title=None, opts=[], data = None, model:CrudEntityModel=None):
    def __init__(
        self,
        get_id,
        entity_name,
        sample,
        head_names,
        title=None,
        opts={},
        data=None,
    ):
        self.title = title
        self.entity_name = entity_name
        self.sample = sample
        self.head_names = head_names
        self.data = data
        if isinstance(get_id, str):
            self.get_id = lambda row: row[get_id]
        elif "function" in str(type(get_id)):
            self.get_id = get_id
        else:
            raise IlegalTableArgument(
                "Table requires that 'get_id' argument to be of type str or function."
            )
        self.opts = opts
        self.aux_head_names = None

    def toTable(self, data: list[dict[str]]):
        sample = self.sample
        if not data and not sample:
            raise BuildViewError("Se requiere al menos el data o sample.")
        if not data:
            # aux_data = {}
            # for key in sample:
            #     aux_data[key] = ""
            # data = [aux_data]
            data = []
        if data and not (isinstance(data, list) and isinstance(data[0], dict)):
            raise BuildViewError(
                "Table view requires that 'data' argument with type list[dict[str]]."
            )
        if not sample and data[0]:
            sample = data[0]
        auxdata = []
        for row in data:
            newrow = {}
            for key in sample:
                if key in row:
                    newrow[key] = row[key]
                else:
                    raise UnvalidateValueException(key, row.get(key))
            auxdata.append(newrow)
        if auxdata:
            viewdata = auxdata
        else:
            viewdata = data
        if self.head_names is None:
            if self.aux_head_names is None:
                names = list(sample.keys())
                auxnames = []
                for name in names:
                    name = name.replace("_", " ").capitalize()
                    auxnames.append(name)
                self.aux_head_names = auxnames
            self.head_names = self.aux_head_names

        opts = []
        if self.opts:
            for kopt in self.opts:
                opt = self.opts[kopt]
                opts.append(opt.toMetaData())
        table_data = {
            "title": self.title,
            "head_names": self.head_names,
            "data": data,
            "viewdata": viewdata,
            "opts": opts,
            "get_id": self.get_id,
            "entity_name": self.entity_name,
        }
        print(f"DATAAAAAAAA {self.entity_name }")
        print(table_data["data"])
        print(f"TAMPLATEEEEEEE {self.entity_name }")
        print(table_data)
        return table_data


class ViewConfig:
    def __init__(self, form: FormView = None, table: TableView = None):
        if not table or not form:
            raise IlegalCrudViewArgument(
                "CrudView requires arguments 'form: FormView' and 'table:TableView' to be types FormView and TableView"
            )
        self.form = form
        self.table = table
        self.form_config = form.toForm(None)
        self.table_config = table.toTable(None)

    def getTitle(self):
        return self.form.getTitle()

    def onTableData(self, data: list[dict[str]]):
        self.table_config = self.table.toTable(data)

    def onFormData(self, data: dict[str], endpoint_name=None):
        self.form_config = self.form.toForm(data, endpoint_name)

    def toTemplate(self):
        print("ViewConfig: self.form_config")
        print(self.form_config)
        template_data = {
            "title": self.form.getTitle(),
            "form_data": self.form_config,
            "table_data": self.table_config,
        }
        return template_data


class ViewFactory:
    @staticmethod
    def tableFromEntity(entity_class):
        return TableView(
            get_id=entity_class.id_name,
            entity_name=entity_class.entity_name,
            sample=entity_class._sample_registrable_model(),
            head_names=None,
        )

    @staticmethod
    def formFromEntity(entity_class):
        sample = entity_class._sample_registrable_model()
        print("--- ViewFactory: SAMPLE:")
        print(sample)
        return FormView(
            sample=sample,
            colrequireds=entity_class.requireds,
            coldisableds=entity_class.disableds,
            enums=entity_class.enums,
            entity_name=entity_class.entity_name,
            enumsmuliple=entity_class.enumsmuliple,
        )
